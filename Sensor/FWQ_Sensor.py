from kafka import KafkaConsumer
from kafka import KafkaProducer
import sys
import random
import time
import threading
import traceback

personas = 0

#Funcion para recibir mensajes de Engine
def esperaEngine(id,server,puerto):
    global personas
    consumer = KafkaConsumer(
        '%s' %(id),
        bootstrap_servers=['%s:%s'%(server,puerto)],
    )

    for msg in consumer:
        print(msg.value)
        personas += 1 

#Funcion para enviar mensajes al servidor de tiempos
def enviarPersonas(id,server,puerto):
    global personas

    producer = KafkaProducer(bootstrap_servers=['%s:%s' %(server,puerto)])
    mensaje = '%s:%s' %(id,str(personas))
    producer.send('sensorPersonas', bytes(mensaje,'UTF-8'))
    producer.flush()

#Funcion utilizada para threading
#Crea un nuevo hilo que ejecuta la funcion enviarPersonas() cada x segundos aleatorios
def every(id,server,puerto):
    delay = random.randint(1,3)
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            enviarPersonas(id,server,puerto)
        except Exception:
            traceback.print_exc()
        delay = random.randint(1,3)
        next_time += delay

#Funcion principal
def main():

    if(len(sys.argv) != 4):
        print("Para ejecutar utiliza: FWQ_Sensor.py |IP SERVER| |PUERTO| |ID ATRACCION|")
    else:
        server = sys.argv[1]
        puerto = sys.argv[2]
        id = sys.argv[3]
        personas = 0

        threading.Thread(target=lambda: every(id,server,puerto)).start()

        esperaEngine(id,server,puerto)


#------------------------
if __name__=="__main__":
    main()