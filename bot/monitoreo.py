from librouteros import connect
import routeros_api


def conectar_router(router):
    connection = routeros_api.RouterOsApiPool(router[2],username=router[0],password=router[1],port=8728)
    api = connection.get_api()
    return api

def crear_plan(router,nombre, vel_subida, vel_bajada):
	api = conectar_router(router)
	lista_planes = api.get_resource('/ip/hotspot/user/profile')
	lista_planes.add(name=nombre, rate_limit=vel_subida+'M/'+vel_bajada+'M', session_timeout='10m', shared_users='2')

def eliminar_plan(router,nombre):
	api = conectar_router(router)
	lista_planes = api.get_resource('/ip/hotspot/user/profile')
	id_plan= lista_planes.get(name=nombre)[0]['id']
	lista_planes.remove(id=id_plan)

def editar_plan(router,nombre, nombre_nuevo, vel_subida, vel_bajada):
	api = conectar_router(router)
	lista_planes = api.get_resource('/ip/hotspot/user/profile')
	id_plan= lista_planes.get(name=nombre)[0]['id']
	lista_planes.set(id=id_plan,name=nombre_nuevo, rate_limit=vel_subida+'M/'+vel_bajada+'M')

def esta_activo(router,usuario):
	api = conectar_router(router)
	lista_activos = api.get_resource('/ip/hotspot/active')
	activo = lista_activos.get(user=usuario)
	if 	activo:
		return True
	else:
		return False

#-------------------------------------------------------------------------------------------------------------------------#

def monitor(router,interfaz):
	api = connect(username=router[0], password=router[1], host=router[2])
	params = {'interface':interfaz,'once':True}
	subida_kbps=api(cmd='/interface/monitor-traffic',**params)[0]['tx-bits-per-second']/1024
	bajada_kbps=api(cmd='/interface/monitor-traffic',**params)[0]['rx-bits-per-second']/1024
	return (bajada_kbps, subida_kbps)

def get_ISP(router,interfaz):
	api = conectar_router(router)
	lista_interfaces = api.get_resource('/ip/route')
	interface= lista_interfaces.get()
	return interface
		

def run_script(router,script):
	api = connect(username=router[0], password=router[1], host=router[2])
	api = conectar_router(router)
	script= '*'+str(script)
	params = {'.id': script} # id script backup
	script=api(cmd='/system/script/run', **params)

def test_ab(router):
	api = connect(username=router[0], password=router[1], host=router[2])
	btest_server= '50.235.23.218'
	btest_user= 'btest'
	btest_pass= 'btest'
	params = {'address':btest_server, 'direction': 'both', 'user': btest_user, 'password': btest_pass, 'duration':'15s'}
	velocidad=api(cmd='/tool/bandwidth-test',**params)
	velocidad_subida= velocidad[16]['tx-current']/1024
	velocidad_bajada= velocidad[16]['rx-current']/1024
	return (velocidad_bajada,velocidad_subida)

def router_status(router):
	api = connect(username=router[0], password=router[1], host=router[2])
	recursos= api(cmd='/system/resource/print')
	return recursos

def usuarios_activos_hotspot(rotuer):
	api = connect(username=router[0], password=router[1], host=router[2])
	usuarios=api(cmd='/ip/hotspot/active/print')
	return usuarios

def ping(router,direccion):
	api = connect(username=router[0], password=router[1], host=router[2])
	params= {'count': '5', 'address':direccion}
	ping= api(cmd='/ping', **params)
	return ping

def trafico_x_cola(router,usuario):
	api = connect(username=router[0], password=router[1], host=router[2])
	params= {'stats':True}
	colas= api(cmd='/queue/simple/print', **params)
	for c in colas:
		if c['name']==usuario:
			rate= c['rate'].split('/')   # subida / bajada
			plan= c['max-limit'].split('/')
			porc_bajada= (int(rate[1])*100)/int(plan[1])
			return '{:.2f}'.format(porc_bajada)
	return False

def backup_router(router):
	api = connect(username=router[0], password=router[1], host=router[2])
	params_back= {'name':'backup_API'}
	params_export={'file':'export_API'}
	backup= api(cmd='/system/backup/save', **params_back)
	export= api(cmd='/export',**params_export)

def send_email(router,email):
# tool e-mail send to=gera_riv@hotmail.com file=
# backup_API.backup,export_API.rsc from=backups@comtik.com.ar subject=Ba
# ckup-COMTIK body=EQUIPO-COMTIK
	api = connect(username=router[0], password=router[1], host=router[2])
	params={'to':email,'file':'backup_API.backup,export_API.rsc', 'from':'backups@comtik.com.ar' ,'subject':'Backups-COMTIK', 'body':'EQUIPO-COMTIK'}
	enviar= api(cmd='/tool/e-mail/send',**params)

def get_file(archivo):
	api = connect(username=router[0], password=router[1], host=router[2])
	archivos= api(cmd='/file/print')
	for a in archivos:
		if a['name']==archivo:
			return a
	
	return False

router= ['gadmin','Dpto1F','192.168.99.20']
#crear_plan(router,'3Megas', '1','3')
#eliminar_plan(router,'4Megas')
#editar_plan(router,'3Megas', '4Megas','2','4')

interfaz= 'wlan1'
#router= ['comtik','ComRou912*/','192.168.10.1']
#velocidad=(54.32526397705078,6.477363586425781)
#print('Bajada: {:.2f}Mbps \nSubida: {:.2f}Mbps'.format(velocidad[0], velocidad[1]))


#consumo= monitor(router,interfaz)
#print('Trafico en la Interfaz: ' + interfaz)
#print('Bajada: {:.2f}kbps'.format(consumo[0]))
#print('Subida: {:.2f}Kbps'.format(consumo[1]))
#marca=router_status(router)[0]['platform'] 
#modelo= router_status(router)[0]['board-name']
#cant_cpu= router_status(router)[0]['cpu-count']
#cpu_load= router_status(router)[0]['cpu-load']
#print('Router: {} {}\nCantidad de CPUs: {}\nCarga de CPU: {}% \nMemori Libre: {}MiB'.format(marca,modelo,cant_cpu,cpu_load,memoria_libre))

#l=esta_activo(router,'3')[0]
#print(l['user'],int(l['bytes-in'])*8/1024/1024,int(l['bytes-out'])*8/1024/1024) # subida / bajada
#datos_ping=ping(router,'8.8.8.8')[0]
#latencia= datos_ping['avg-rtt']
#pkt_perdidos= datos_ping['packet-loss']
#print(latencia,pkt_perdidos)

#print(trafico_x_cola(router,'user1'))

#send_email(router,'gera_riv@hotmail.com')

#print(get_ISP(router,'ether3'))

