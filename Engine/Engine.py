from concurrent import futures

import logging
import grpc

#Le pasa el mapa a WaitingTimeServer al conectarse.
#Registra los pasos de los visitantes en el mapa.
#Envía el mapa actualizado a los usuarios.

#argumentos:
#o IP y puerto del broker/Bootstrap-server del gestor de colas
#o Número máximo de visitantes
#o IP y puerto del FWQ_WatingTimeServer

