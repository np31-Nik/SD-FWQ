from concurrent import futures
from google.protobuf import message
from kafka import KafkaConsumer
import logging
import grpc
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'WaitingTimeServer'))
import TimeServer_pb2
import TimeServer_pb2_grpc
import numpy as np
import time
import traceback
import threading

tiempos = np.full((2,2),0)
#tiempos = [["a1",0],["a2",0]]
usuariosEspera = []
num_atr=0
atr = np.full((num_atr,3),'---')
num_atr=0
primera = True

class Time(TimeServer_pb2_grpc.CalculateTimeServicer):
	def Time(self,request,context):
		global num_atr,atr,tiempos
		resul=tiempos.tobytes()
		ej = np.full((num_atr,3),'---')
		
		num_atr=request.num_atra
		
		atr= np.frombuffer(request.atr, dtype=ej.dtype).reshape(num_atr,3)
		return TimeServer_pb2.TimeResponse(times=resul,len=len(tiempos))


# def ObtenerTiempo():
#     channel = grpc.insecure_channel('localhost:50051')
#     #channel = grpc.insecure_channel('192.168.4.246:50051')
#     stub = TimeServer_pb2_grpc.CalculateTimeStub(channel)
#     response = stub.Registry(TimeServer_pb2.RegistryRequest(ID=1,name="you",password="12345"))
#     print("Client received: " + response.response)
# class WaitingTime(object):
#     def WaitingTimeServer(self,request,context):
# 		return WaitingTimeServer.WaitingTimeServerResponse(response=calcularTiempo())
#     def calcularTiempo():

def generarTiempos():
	global tiempos
	tiempos = np.full((num_atr,2),'---')
	for i in range(num_atr):
		tiempos[i][0] = atr[i][0]
		tiempos[i][1] = atr[i][2]
	
	
def actualizarTiempos(id_atr,personas,anyadir):
	global tiempos
	global usuariosEspera
	global primera
	d=True
	if anyadir:
		if primera:
			generarTiempos()
			primera=False

		index = -1

		for i in range(0,num_atr):

			if atr[i][0] ==id_atr:
				index = i
				break
		#index = np.where(atr[:,0] == id_atr)
		if index > 0:
			datos = atr[index]
			d=True
		else:
			datos = 0
			d=False
	if not primera and d:
		for i in range(num_atr):
			if len(tiempos)>0:
				if tiempos[i][0] == id_atr:
					if anyadir:
						ciclos = int(np.ceil(float(len(personas))/float(datos[1])))
						tiempo = ciclos * int(datos[2])
						if tiempo > 0:
							tiempos[i][1]=tiempo
					else:
						if tiempos[i][1] > int(datos[2]):
							tiempos[i][1] = int(tiempos[i][1]) - 1

							#esto depende de si hay que mostrar el tiempo para cada usuario:
							# for i in len(usuariosEspera):
							# 	if usuariosEspera[i][1] > 0:
							# 		usuariosEspera[i][1] -= 1
							# 	else:
							# 		del usuariosEspera[i]
	#if anyadir or not primera:
		

def reloj():
	delay = 1
	next_time = time.time() + delay
	while True:
		time.sleep(max(0, next_time - time.time()))
		try:
			for i in range(num_atr):
				actualizarTiempos(i,0,False)
		except Exception:
			traceback.print_exc()
		next_time += delay

			
def escuchaSensor(server,puerto):
	
	consumer = KafkaConsumer(
        'sensorPersonas',
        bootstrap_servers=['%s:%s'%(server,puerto)],
    )

	for msg in consumer:
		datos=msg.value.decode('UTF-8').split(':')
		actualizarTiempos(datos[0],datos[1],True)
		

def escuchaEngine(puerto):

	server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
	TimeServer_pb2_grpc.add_CalculateTimeServicer_to_server(Time(),server)
	server.add_insecure_port('[::]:%s'%(puerto))
	server.start()
	server.wait_for_termination()



def main():

	if(len(sys.argv) != 4):
		print("Para ejecutar utiliza: FWQ_WaitingTimeServer.py |PUERTO ESCUCHA| |IP GESTOR| |PUERTO GESTOR|")
	else:
		puerto_escucha = sys.argv[1]
		ip_gestor = sys.argv[2]
		puerto_gestor = sys.argv[3]
		personas = 0

		t=threading.Thread(target = escuchaEngine, args=(puerto_escucha,))
		threading.Thread(target = escuchaSensor, args=(ip_gestor,puerto_gestor)).start()
		threading.Thread(target = reloj).start()
		t.start()
		t.join()







#------------------------
if __name__=="__main__":
    main()




