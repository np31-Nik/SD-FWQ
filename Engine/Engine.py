from kafka import KafkaConsumer
from kafka import KafkaProducer

#mapa en bloc de notas (SI)

pasos = KafkaConsumer('sample')
for message in pasos:
    print (message)
    producer = KafkaProducer(bootstrap_servers='192.168.3.246:9092')
    producer.send('respuesta', b'hola!')
    print("Hola")

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

