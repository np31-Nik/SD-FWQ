from concurrent import futures

import logging
import grpc
class WaitingTime(object):
    def WaitingTimeServer(self,request,context):
		return WaitingTimeServer.WaitingTimeServerResponse(response=calcularTiempo())

    def calcularTiempo():








