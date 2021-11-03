from concurrent import futures
from kafka import KafkaConsumer
import logging
import grpc
import sys
<<<<<<< HEAD
sys.path.append('C:/Users/serge/source/repos/SD-FWQ/WaitingTimeServer')
import TimeServer_pb2
import TimeServer_pb2_grpc

def ObtenerTiempo():
    channel = grpc.insecure_channel('localhost:50051')
    #channel = grpc.insecure_channel('192.168.4.246:50051')
    stub = TimeServer_pb2_grpc.CalculateTimeStub(channel)
    response = stub.Registry(TimeServer_pb2.RegistryRequest(ID=1,name="you",password="12345"))
    print("Client received: " + response.response)
# class WaitingTime(object):
#     def WaitingTimeServer(self,request,context):
# 		return WaitingTimeServer.WaitingTimeServerResponse(response=calcularTiempo())
#     def calcularTiempo():
=======

# class WaitingTime(object):
#     def WaitingTimeServer(self,request,context):
# 		return WaitingTimeServer.WaitingTimeServerResponse(response=calcularTiempo())

#     def calcularTiempo():

def escuchaSensor():
  	print("hola q tal")

def main():
	if(len(sys.argv) != 4):
		print("Para ejecutar utiliza: FWQ_WaitingTimeServer.py |PUERTO ESCUCHA| |IP GESTOR| |PUERTO GESTOR|")
  	else:
		puerto_escucha = sys.argv[1]
		ip_gestor = sys.argv[2]
		puerto_gestor = sys.argv[3]
		personas = 0

		escuchaSensor()

		#escuchaEngine()



#------------------------
if __name__=="__main__":
    main()








>>>>>>> 0f1cd56ce797967580cdfc8469611509756309c2




