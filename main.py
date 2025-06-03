from background import keep_alive
import telebot
from astrotools import *
bot = telebot.TeleBot('7678574185:AAFvlXq2-t1sprK_mxHAchiJ9soSNVwK7mw')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, 'Привет, я астрологический бот.Напиши /help для списка команд.')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    text = message.text.split(',')
    if text[0] == "Натальная карта":
        try:
            res = natal(datetime(int(text[1]),
                                int(text[2]),
                                int(text[3]),
                                int(text[4]),
                                int(text[5])),
                                float(text[6]),
                                float(text[7]))
            bot.send_photo(message.chat.id, photo=open(res[0], 'rb'))
            print(res[1])
            for i in res[1].split('\n'):
                if i != '':
                    bot.send_message(message.from_user.id, i)
        except:
                bot.send_message(message.from_user.id, "Что-то не так. Попробуй снова")
    elif text[0] == "/help":
        with open('help.txt', 'rb') as f:
            bot.send_message(message.from_user.id, f.read())
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
keep_alive()
bot.polling(none_stop=True, interval=0)
