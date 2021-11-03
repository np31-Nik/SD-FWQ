from kafka import KafkaConsumer
from kafka import KafkaProducer
import sys
import random
import time
import threading

#Funcion para recibir mensajes de Engine
def esperaEngine(id,server,puerto,personas):

    #Usar paralelismo para escuchar y enviar a la vez??
    #
    #
    #
    
    consumer = KafkaConsumer(
        '%s' %(id),
        bootstrap_servers=['%s:%s'%(server,puerto)],
    )
    waitTime = random.randInt(1,3)
    t = threading.Timer(waitTime,enviarTiempos(id,server,puerto,personas))

    for msg in consumer:
        print(msg)
        personas += 1 

    return personas

#Funcion para enviar mensajes al servidor de tiempos
def enviarTiempos(id,server,puerto,personas):

    producer = KafkaProducer(bootstrap_servers=['%s:%s' %(server,puerto)])
    producer.send('sensorPersonas', b'%s:%s' %(id,str(personas)))
    producer.flush()

#Funcion principal
def main():

    # print(f"Arguments count: {len(sys.argv)}")
    # for i, arg in enumerate(sys.argv):
    #     print(f"Argument {i:>6}: {arg}")
    if(len(sys.argv) != 4):
        print("Para ejecutar utiliza: FWQ_Sensor.py |IP SERVER| |PUERTO| |ID ATRACCION|")
    else:
        server = sys.argv[1]
        puerto = sys.argv[2]
        id = sys.argv[3]
        personas = 0

        personas = esperaEngine(id,server,puerto,personas)
        enviarTiempos(id,server,puerto,personas)



#------------------------
if __name__=="__main__":
    main()