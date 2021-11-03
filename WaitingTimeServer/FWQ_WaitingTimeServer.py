from concurrent import futures

import logging
import grpc
import sys
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




