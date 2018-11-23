import os

from flask import Flask, request

import telebot
from telebot import types

import sketch
TOKEN = '632985476:AAFfx7TD5eeKRhgexKBgMERA6zgD7znLFD4'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(commands=['menu'])
def open_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('/youtube')
    btn2 = types.KeyboardButton('/sketch')
    btn3 = types.KeyboardButton('/c')
    btn4 = types.KeyboardButton('/d')
    markup.add(btn1,btn2,btn3,btn4)
    bot.reply_to(message,"Choose One letter:",reply_markup=markup)

@bot.message_handler(commands=['youtube','sketch','c','d'])
def menu_handler(message):
    if message.text == '/youtube':
        bot.reply_to(message,'You have selected '+message.text)
    elif message.text == '/sketch':
        msg = bot.send_message(message.from_user.id,'Send me your photo')
        bot.register_next_step_handler(msg,photo_sketch)

def photo_sketch(message):
    bot.send_mesasge(message.from_user.id,message)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://sheltered-earth-64926.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
