#-- coding: utf-8 --
import telebot
import json
import urllib.request

#TOKEN DO BOT
API_TOKEN = ''

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['cep'])
def send_cep(message):
    msg = bot.reply_to(message, """Digite o CEP que deseja consultar:""")
    cid = message.chat.id #id da conversa
    bot.register_next_step_handler(msg, send_cep_step) # a mensagem digitada, vai ser atribuida a variavél message_cep

def send_cep_step(message):
    cid = message.chat.id
    mensagem_cep = message.text 
    url = "https://viacep.com.br/ws/" + mensagem_cep + "/json/"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    cep = data['cep']
    logradouro = data['logradouro']
    bairro = data['bairro']
    localidade = data['localidade']
    uf = data['uf']
    
    bot.send_message(cid, "CEP: " + cep + "\nLogradouro: " + logradouro + "\nBairro: " + bairro + "\nLocalidade: " + localidade + "\nUF: " + uf)


bot.polling()
    


    
