from concurrent import futures
from google.protobuf import message
from kafka import KafkaConsumer
import logging
import grpc
import sys
sys.path.append('C:/Users/serge/source/repos/SD-FWQ/WaitingTimeServer')
import TimeServer_pb2
import TimeServer_pb2_grpc

def CalcularTiempo():
    return 1

class Time(TimeServer_pb2_grpc.CalculateTimeServicer):
	def Time(self,request,context):
		resul=CalcularTiempo()
		return TimeServer_pb2.TimeResponse(message=str(resul))

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




