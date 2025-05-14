
import telebot
from astrotools import *
bot = telebot.TeleBot('')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    text = message.text.split(',')
    if text[0] == "Натальная карта":
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
    elif text[0] == "/help":
        with open('help.txt', 'rb') as f:
            bot.send_message(message.from_user.id, f.read())
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)