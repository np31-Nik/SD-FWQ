from kafka import KafkaConsumer
from kafka import KafkaProducer
import time

#mapa en bloc de notas (SI)


pasos = KafkaConsumer(
    'h',
    bootstrap_servers=['192.168.3.246:9092'],
)

for message in pasos:
    print (message)
    time.sleep(1)
    producer = KafkaProducer(bootstrap_servers=['192.168.3.246:9092'])
    producer.send('respuesta', b'hola que tal')
    producer.flush()
    print("Hola")
pasos.close()


#producer.send('respuesta', b'hola que tal')
#producer.flush()

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

