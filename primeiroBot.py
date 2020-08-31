#-- coding: utf-8 --
import telebot
from telebot import types

#Token do bot
API_TOKEN = '1158156083:AAGUm2ojTv6yZKq18EyTY4CWOWzKbFBgckw'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_start(message):
	cid = message.chat.id
	bot.send_message(cid, "Funcionou")

bot.polling() #Fica verificando as mensagens
