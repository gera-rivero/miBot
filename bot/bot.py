import telebot
from telebot import types
from monitoreo import send_email
import time
from consultas_de_red import *


TOKEN = ''

bot= telebot.TeleBot(TOKEN)


actionSelect = types.ReplyKeyboardMarkup(one_time_keyboard=False,resize_keyboard=True,row_width=1) 
actionSelect.row('📊 Estado de Conexión 📊')
actionSelect.row('📈 Trafico Actual 📈')
actionSelect.row("💾 Backup Router 💾")


clientes_habilitados= {
        }


def backup(bot,msj,chat_id,datos_cliente):
	funcion= '\nvamos a resguardar toda la configuración de tu router, dame unos segundos 👉⏱'
	saludo = '{}, {}'.format(msj.from_user.first_name,funcion)
	
	bot_escribiendo(bot,chat_id,1) 
	bot.send_message(chat_id= msj.chat.id, text=saludo)	

	router= datos_cliente[:3]
	backup_router(router)
	respuesta= 'Tu backup se realizó correctamente, gracias por confiar en mi 😊'
		
	bot_escribiendo(bot,chat_id,2)
	bot.send_message(chat_id= chat_id, text=respuesta)

	msg = bot.reply_to(msj, "Por las dudas, quieres que te envie el archivo de backup por mail? 📧",reply_markup=actionConfirm)
	bot.register_next_step_handler(msg, process_mail_step)

def process_mail_step(message):
    try:
        chat_id = message.chat.id
        respuesta = message.text
        if respuesta=='SI':
        	msg = bot.reply_to(message, 'Me decis la direccion de correo, por favor? ejemplo: micorreo@botcito.com 😉',reply_markup=actionSelect)
        	bot.register_next_step_handler(msg, process_envio_step)
        if respuesta=='NO':
        	texto= 'Perfecto {}, queda guardado igualmente en tu router, me alegra haberte ayudado.\nSaludos'.format(message.from_user.first_name)
        	bot.send_message(chat_id=chat_id, text=texto,reply_markup=actionSelect)
    except Exception as e:
    	bot.reply_to(message,'Mmm disculpa, no me estarías contestando lo que te pregunte 🤔')

def process_envio_step(message):
    chat_id = str(message.chat.id)
    correo = message.text
    datos_cliente= clientes_habilitados.get(chat_id,False)
    router= datos_cliente[:3]
    send_email(router,correo)
    texto= 'Perfecto {}, en unos instantes recibirás los archivos de configuración resguardados en el correo que me pasaste.\nFeliz de ayudarte 😊😊😊'.format(message.from_user.first_name)
    bot.send_message(chat_id=chat_id, text=texto,reply_markup=actionSelect)


@bot.message_handler(commands=['comenzar'])
def iniciar(msj):
	chat_id= str(msj.chat.id)
	datos_cliente= clientes_habilitados.get(chat_id,False)
	if datos_cliente:	
		#saludar(msj)
		bot.send_message(chat_id, "Hola {}, en que te puedo ayudar?".format(msj.from_user.first_name), reply_markup=actionSelect)
	else:
		bot_escribiendo(bot,chat_id,2)
		bot.send_message(chat_id= chat_id, text='Lo siento no dispones de esta funcionalidad')

@bot.message_handler(func=lambda message: message.text == "📈 Trafico Actual 📈")
def mostrar_trafico(msj):
	chat_id= str(msj.chat.id)
	datos_cliente= clientes_habilitados.get(chat_id,False)
	if datos_cliente:
		consultar_trafico(bot,msj,chat_id,datos_cliente)
	else:
		bot_escribiendo(bot,chat_id,2)
		bot.send_message(chat_id= chat_id, text='Lo siento no dispones de esta funcionalidad')

@bot.message_handler(func=lambda message: message.text == "📊 Estado de Conexión 📊")
def mostrar_estado_conexion(msj):
	chat_id= str(msj.chat.id)
	datos_cliente= clientes_habilitados.get(chat_id,False)
	if datos_cliente:
		consultar_estado_conexion(bot,msj,chat_id,datos_cliente)
	else:
		bot_escribiendo(bot,chat_id,2)
		bot.send_message(chat_id= chat_id, text='Lo siento no dispones de esta funcionalidad')


@bot.message_handler(func=lambda message: message.text == "💾 Backup Router 💾")
def backupear_router(msj):
	chat_id= str(msj.chat.id)
	datos_cliente= clientes_habilitados.get(chat_id,False)
	if datos_cliente:
		backup(bot,msj,chat_id,datos_cliente)
	else:
		bot_escribiendo(bot,chat_id,2)
		bot.send_message(chat_id= chat_id, text='Lo siento no dispones de esta funcionalidad')
	

# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
	bot.send_message(m.chat.id, "Perdon no entiendo tu consulta sobre \"" + m.text + "\"\nPuedes probar escribiendo /comenzar")

bot.infinity_polling(True)
