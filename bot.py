import telebot
from telebot import types
from parser2 import *

bot = telebot.TeleBot('6791128966:AAEbFKCPtde9NOEIwQAhYzYjEA3VE6eBqzk')

@bot.message_handler(commands=['start'])
def start(message):
    start_message = 'Привет! Этот бот может показать тебе оценки преподавателей с wiki.mipt.\n\nПро кого ты хочешь узнать?'
    bot.send_message(message.chat.id, start_message)

@bot.message_handler()
def request(message):
    req = str(message.text.lower())
    req = req.replace('ё', 'е')
    req = req.split()
    answer = search(req)
    bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True)
