from concurrent import futures
from google.protobuf import message
from kafka import KafkaConsumer
import logging
import grpc
import sys
sys.path.append('C:/Users/serge/source/repos/SD-FWQ/WaitingTimeServer')
import TimeServer_pb2
import TimeServer_pb2_grpc
import numpy as np

tiempos = []
def CalcularTiempo():
	message = 'Python is fun'
	# convert string to bytes
	byte_message = bytes(message, 'utf-8')
	print(byte_message)
	return byte_message

class Time(TimeServer_pb2_grpc.CalculateTimeServicer):
	def Time(self,request,context):
		resul=CalcularTiempo()
		return TimeServer_pb2_grpc.TimeResponse(message=resul)
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

def generarTiempos(num_atr,atracciones):
	global tiempos
	tiempos = np.full((num_atr,2),0)
	for i in range(num_atr):
		tiempos[i][0] = atracciones[i]

	print(tiempos)

def actualizarTiempos(id_atr,num_atr,atr):
	global tiempos
	datos = atr[np.where(atr[:,0] == id_atr)]

	for i in range(num_atr):
		if tiempos[i][0] == id_atr:
			print("hola")

			
def escuchaSensor(server,puerto):
	global personas
	consumer = KafkaConsumer(
        'sensorPersonas',
        bootstrap_servers=['%s:%s'%(server,puerto)],
    )

	for msg in consumer:
		#print(msg)
		datos=msg.value.decode('UTF-8').split(':')
		print(datos)

def main():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	TimeServer_pb2_grpc.add_CalculateTimeServicer_to_server(Time(),server)
	server.add_insecure_port('[::]:50051')
	server.start()
	server.wait_for_termination()

	return True
	# if(len(sys.argv) != 4):
	# 	print("Para ejecutar utiliza: FWQ_WaitingTimeServer.py |PUERTO ESCUCHA| |IP GESTOR| |PUERTO GESTOR|")
  	# else:
	# 	puerto_escucha = sys.argv[1]
	# 	ip_gestor = sys.argv[2]
	# 	puerto_gestor = sys.argv[3]
	# 	personas = 0

	# 	escuchaSensor()

	# 	#escuchaEngine()



#------------------------
if __name__=="__main__":
    main()




