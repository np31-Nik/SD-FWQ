from kafka import KafkaConsumer
from kafka import KafkaProducer
import time
import sqlite3
import numpy as np

#Funcion para conectarnos a la BD
def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except:
        print('Hubo un problema conectando a la BD.')

    return conn

#Funcion que obtiene el array del mapa desde la BD
def get_mapa(c,id_mapa):

    c.execute("""SELECT * FROM Mapa where id='%s'""" %(id_mapa))
    mapa = c.fetchall()
    return mapa

#Funcion que obtiene el array de atracciones desde la BD
def get_atracciones(c,mapa):

    atracciones = []
    for atr in mapa:
        c.execute("""SELECT * FROM atracciones where id='%s'""" %(atr[3]))
        query = c.fetchall()
        atracciones.append(query[0])

    return atracciones

#Funcion que imprime el mapa por consola
def print_mapa(matriz):

    for i in range(0,19):
        for j in range(0,19):
            print("\t{0}".format(matriz[i][j]),sep=',',end='')
        print('')

#Funcion que crea una matriz para visualizar el mapa
def rellenar_mapa(mapa):

    matriz = np.full((20,20), '---')

    for atr in mapa:
        x = atr[1]
        y = atr[2]
        matriz[x][y] = atr[3]

    return matriz

#Funcion principal
def main():

    conn = create_connection('db.db')
    c=conn.cursor()

    id_mapa = 'm1'

    mapa = get_mapa(c,id_mapa)
    atracciones = get_atracciones(c,mapa)

    matriz = rellenar_mapa(mapa)
    #print_mapa(matriz)




# pasos = KafkaConsumer(
#     'h',
#     bootstrap_servers=['192.168.3.77:9092'],
# )

# for message in pasos:
#     print (message)
#     time.sleep(1)
#     producer = KafkaProducer(bootstrap_servers=['192.168.3.77:9092'])
#     producer.send('respuesta', b'hola que tal')
#     producer.flush()
#     print("Hola")
# pasos.close()


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



#------------------------
if __name__=="__main__":
    main() 