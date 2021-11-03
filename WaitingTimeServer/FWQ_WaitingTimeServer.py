from concurrent import futures
from kafka import KafkaConsumer
import logging
import grpc
import sys

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












