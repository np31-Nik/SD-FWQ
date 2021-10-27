from concurrent import futures

import logging
import grpc
import Registry_pb2
import Registry_pb2_grpc

#hola che
class Registry(Registry_pb2_grpc.RegistryServiceServicer):
	def Registry(self,request,context):
		print("Recibiendo")
		return Registry_pb2.RegistryResponse(response="Usuario anyadido a la base de datos(No)")


def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	Registry_pb2_grpc.add_RegistryServiceServicer_to_server(Registry(), server)
	server.add_insecure_port('[::]:50051')
	server.start()
	server.wait_for_termination()


if __name__ == '__main__':
	logging.basicConfig()
	serve()
