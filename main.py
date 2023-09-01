import telebot
from telebot import types
import random
import re

token = '___' #сюда вставить TOKEN
bot = telebot.TeleBot(token)
info = 'Угадай слово, называя по одной букве или слово целиком. У тебя будет 8 попыток.'
words_list = ['Сфинкс', 'Кордебалет', 'Формуляр', 'Хроника', 'Галера', 'Кафель', 'Фильтр', 'Башня', 'Кондитер',
              'Тетерев', 'Камбала', 'Самовар']
result = '0'
counter = [0]


@bot.message_handler(commands=['start'])
def greeting(message):
    name = message.from_user.first_name
    bot.send_message(message.chat.id, f'Привет, {name}! Я бот, который умеет играть в угадайку.')
    markup = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton('ИГРАТЬ', callback_data='play')
    button_2 = types.InlineKeyboardButton('ПРАВИЛА ИГРЫ', callback_data='help')
    markup.row(button_1, button_2)
    bot.send_message(message.chat.id, text='Выбери:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'help')
def rules(callback_obj):
    bot.send_message(callback_obj.from_user.id, info)
    bot.answer_callback_query(callback_query_id=callback_obj.id)


@bot.callback_query_handler(func=lambda call: call.data == 'play')
def start_play(callback_obj):
    bot.send_message(callback_obj.from_user.id, 'Давай играть')
    bot.answer_callback_query(callback_query_id=callback_obj.id)
    global result
    global hidden_result
    global counter
    counter = [0]
    result = random.choice(words_list)
    hidden_result = [' _ ' for _ in range(len(result))]
    bot.send_message(callback_obj.from_user.id, ''.join(hidden_result))


@bot.message_handler(content_types=['text'])
def guess(message):
    global result
    global counter
    if result == '0':
        bot.send_message(message.chat.id, f'Введи /start')
    else:
        counter[0] += 1

        if len(message.text) != 1 and result.lower() != message.text.lower():
            bot.send_message(message.chat.id, f'Не угадал. Осталось {8 - counter[0]} попыток')

        elif message.text.lower() == result.lower():
            bot.send_message(message.chat.id, 'Ты угадал! Если хочешь сыграть еще раз, введи /start')
            result = '0'


        else:
            if message.text.lower() in result.lower():
                matches = re.finditer(message.text.lower(), result.lower())
                indices = [match.start() for match in matches]
                for i in indices:
                    hidden_result[i] = message.text
                if ''.join(hidden_result) == result.lower():
                    bot.send_message(message.chat.id, 'Ты угадал! Если хочешь сыграть еще раз, введи /start')
                    result = '0'

                bot.send_message(message.chat.id, ''.join(hidden_result))
                bot.send_message(message.chat.id, f'Осталось {8 - counter[0]} попыток')

            else:
                bot.send_message(message.chat.id, f'Нет такой буквы. Осталось {8 - counter[0]} попыток')

    if counter[0] == 8 and ''.join(hidden_result).lower() != result.lower():
        bot.send_message(message.chat.id,
                         f'Попытки закончились. Ты проиграл. Было загадано слово {result.upper()}. Если хочешь сыграть еще раз, введи /start')
        result = '0'


bot.polling(non_stop=True)