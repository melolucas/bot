#-- coding: utf-8 --
import requests 
import telebot
from telebot import types
import pymysql #biblioteca de conexao com o MySQL

conn = pymysql.connect(host='127.0.0.1', 
unix_socket='/opt/lampp/var/mysql/mysql.sock', #qual base ele deve se conectar
user='root', #usuario
passwd=None, #vazio
db='usuarios_telegram') #nome do banco de dados

# 127.0.0.1 é igual localhost

cur = conn.cursor() #conexao com o xampp


API_TOKEN = '#@botfather' 

bot = telebot.TeleBot(API_TOKEN) #telebot-sumário e TeleBot(comando) aplicando token

user_dict = {} #variáveis únicas

class User: #minusculo
	def __init__(self,name):
		self.name = name
		self.age = None
		self.team = None
		self.mail = None

@bot.message_handler(commands=['start'])
def send_welcome(message):
	msg = bot.reply_to(message,"Tudo bem? Este é o bot de notícias do Torcedor Apaixonado")#inserindo message
	cid = message.chat.id
	bot.send_message(cid,"Nosso id é: " + str(cid) + " este bot serve para enviar notícias do seu clube do coração,\nQual seu nome?")
	bot.register_next_step_handler(msg,process_name_step) #next

def process_name_step(message):
	try:
		chat_id = message.chat.id
		name = message.text
		user = User(name)
		user_dict[chat_id] = user #armazenando o chat_id desta conversa, único
		msg = bot.reply_to(message,'Quantos anos você tem?')
		bot.register_next_step_handler(msg,process_age_step)
	except Exception as e:
		bot.reply_to(message,e)

def process_age_step(message):
	try:
		chat_id = message.chat.id
		age = message.text
		if not age.isdigit():
			msg = bot.reply_to(message,"Você precisa digitar um número! Quantos anos você tem?")
			bot.register_next_step_handler(msg,process_age_step)
			return
		user = user_dict[chat_id]
		user.age = age
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True) #cria a opção
		markup.add('Gremio','Internacional') #quais as categorias
		msg = bot.reply_to(message, 'Qual o seu time do coração?',reply_markup=markup) #envia a opcao
		bot.register_next_step_handler(msg, process_team_step)
	except Exception as e:
		bot.reply_to(message, 'Oops, algo deu errado')
		print(e)

def process_team_step(message):
	try:
		chat_id = message.chat.id
		team = message.text
		user = user_dict[chat_id]
		if (team == u'Gremio') or (team == u'Internacional'):
			user.team = team
		else:
			raise Exception()
		msg = bot.reply_to(message,'Qual o seu e-mail?')
		bot.register_next_step_handler(msg,process_mail_step)
	except Exception as e:
		bot.reply_to(message,e)

def process_mail_step(message):
	try:
		chat_id = message.chat.id
		mail = message.text
		user = user_dict[chat_id]

		# nome da base
		cur.execute("USE usuarios_telegram") #executando base a ser usada
		sql = "INSERT INTO usuario (nome_usuario,chatid_usuario,categoria_usuario,email_usuario,idade_usuario) VALUES (%s,%s,%s,%s,%s)" #comando
		val = (user.name,str(chat_id),user.team,mail,str(user.age))
		cur.execute(sql,val)#comando insert + valores
		print(val) 
		conn.commit() #ação do comando digitado
		cur.close()
		conn.close()
		msg = bot.reply_to(message,'Obrigado por se cadastrar!')
		
	except Exception as e:
		bot.reply_to(message,e)

bot.enable_save_next_step_handlers(delay=2) # Delay de 2s
bot.load_next_step_handlers()

bot.polling()
