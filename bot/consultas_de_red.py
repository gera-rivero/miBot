from monitoreo import 	monitor, test_ab,ping, backup_router, send_email
from telebot import types
import time


actionConfirm = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True,row_width=1) 
actionConfirm.add('SI', 'NO')


def saludar(bot,mensaje,funcion=''):
	presentacion = 'bienvenido!\nSoy el bot de COMTIK para {}.'.format(mensaje.chat.title)
	saludo = 'Hola {}, {} {}'.format(mensaje.from_user.first_name, presentacion,funcion)
	bot.send_message(chat_id= mensaje.chat.id, text=saludo)

def bot_escribiendo(bot,chat,tiempo):
	bot.send_chat_action(chat, 'typing')  # show the bot "typing" (max. 5 secs)
	time.sleep(tiempo)

def consultar_trafico(bot,msj,chat_id,datos_cliente):
	funcion= '\ndame unos segundos mientras obtengo tu consumo de trafico ⏱'
	saludo = '{}, {}'.format(msj.from_user.first_name,funcion)
	
	bot_escribiendo(bot,chat_id,1) 
	bot.send_message(chat_id= msj.chat.id, text=saludo)	

	interfaz= datos_cliente[3]
	router= datos_cliente[:3]
		
	velocidad=monitor(router,interfaz)
	vel_bajada= velocidad[0]
	vel_subida= velocidad[1]

	if vel_bajada>999:
		vel_bajada= vel_bajada/1024
		vel_bajada= '{:.2f}'.format(vel_bajada) + 'Mbps'
	else: 
		vel_bajada= '{:.2f}'.format(vel_bajada) + 'Kbps'

	if vel_subida>999:
		vel_subida= vel_subida/1024
		vel_subida= '{:.2f}'.format(vel_subida) + 'Mbps'
	else: 
		vel_subida= '{:.2f}'.format(vel_subida) + 'Kbps'

	#TO DO ------------------------------------- Agregar comentarios sobre el consumo de trafico 

	velocidad_actual= '⏬ Tu consumo de Bajada en este momento esta en: {}\n\n⏫ Y el consumo de Subida en unos: {}\n\nEspero haber sido de ayuda, hasta luego.😁👍'.format(vel_bajada, vel_subida)
		
	bot_escribiendo(bot,chat_id,2)
	bot.send_message(chat_id= chat_id, text= velocidad_actual)	


def consultar_estado_conexion(bot,msj,chat_id,datos_cliente):
	funcion= '\naguarda unos segundos mientras evaluo el estado de tu conexión ⏱'
	saludo = '{}, {}'.format(msj.from_user.first_name,funcion)
	
	bot_escribiendo(bot,chat_id,1) 
	bot.send_message(chat_id= msj.chat.id, text=saludo)	

	router= datos_cliente[:3]
	datos_ping=ping(router,'8.8.8.8')[0]
	latencia= datos_ping['avg-rtt']
	pkt_perdidos= datos_ping['packet-loss']
	pkt_loss_percent= (pkt_perdidos*100)/5

	info_ping= '⏳ Tenes una latencia o tiempo de respuesta promedio de unos {} \n\n📉 Un porcentaje de perdida de paquetes del {}%\n'.format(latencia,pkt_loss_percent) 
	bot_escribiendo(bot,chat_id,2)
	bot.send_message(chat_id= chat_id, text= info_ping)
		

	espera= 'Aguarda unos momentos más, mientras mido la velocidad para descargas y subidas...'
		
	bot_escribiendo(bot,chat_id,2)
	bot.send_message(chat_id= chat_id, text=espera)
		
	#TO DO ------------------------------------- Agregar comentarios sobre el estado de la conexion segun latencia perdida de paquetes y velocidades	
	velocidad=test_ab(router)
	vel_bajada= velocidad[0]
	vel_subida= velocidad[1]

	if vel_bajada>999:
		vel_bajada= vel_bajada/1024
		vel_bajada= '{:.2f}'.format(vel_bajada) + 'Mbps'
	else: 
		vel_bajada= '{:.2f}'.format(vel_bajada) + 'Kbps'

	if vel_subida>999:
		vel_subida= vel_subida/1024
		vel_subida= '{:.2f}'.format(vel_subida) + 'Mbps'
	else: 
		vel_subida= '{:.2f}'.format(vel_subida) + 'Kbps'

	velocidad_actual= '⏬ Velocidad de Descarga: {} \n\n⏫ Velocidad de Subida: {}\n\nGracias por tu paciencia, espero haber sido de ayuda, hasta luego.😁👍'.format(vel_bajada, vel_subida)
		
	bot_escribiendo(bot,chat_id,1)  # show the bot "typing" (max. 5 secs)
	bot.send_message(chat_id= chat_id, text= velocidad_actual)
		
	bot_escribiendo(bot,chat_id,2)
	obersvacion= '☝ Un tip: No utilices muy seguido esta función mientras haya personas trabajando en línea, ya que ocupa todo el ancho de banda disponible de tu conexión para una medición mas exacta.'
	bot.send_message(chat_id=chat_id, text=obersvacion)


