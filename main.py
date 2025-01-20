
import telebot
from natal import *
from ai import *
bot = telebot.TeleBot('7678574185:AAFifsjwC5MuFexFf4LkS9Q0DeaRiXR0u08')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    text = message.text.split(',')
    if text[0] == "Натальная карта":
        bot.send_photo(message.chat.id, photo=open(natal_chart(text[1],
                                                               text[2],
                                                               (float(text[3]), float(text[4]))), 'rb'))
    elif text[0] == "Гороскоп":
        bot.send_message(message.from_user.id, ai_request(text[1]))
    elif text[0] == "/help":
        with open('help.txt', 'rb') as f:
            bot.send_message(message.from_user.id, f.read())
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)