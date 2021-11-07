from kafka import KafkaConsumer
from kafka import KafkaProducer
import time
import sqlite3
import numpy as np
import sys
from concurrent import futures
import logging
import grpc

import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'WaitingTimeServer'))
import TimeServer_pb2
import TimeServer_pb2_grpc

import traceback
import threading


#Variable global que almacena las posiciones de los usuarios
posiciones = np.full((2,3),'---')
matriz = []
cola_entrada = []
usuarios_espera = []
visitantes_max = 0
visitantes_actual = 0
pos_atr = []
num_atr=0


def reloj(ip,puerto,atr):
	#print("reloj")
	delay = 1
	next_time = time.time() + delay
	while True:
		time.sleep(max(0, next_time - time.time()))
		try:
			ObtenerTiempo(ip,puerto,atr)
		except Exception:
			traceback.print_exc()
		next_time += delay



#Llamada GRPC al servidor de tiempos de espera
def ObtenerTiempo(ip,port,atra):
    #channel = grpc.insecure_channel('localhost:50051')
    channel = grpc.insecure_channel('%s:%s' %(ip,port))
    stub = TimeServer_pb2_grpc.CalculateTimeStub(channel)
    #print(atra)
    response = stub.Time(TimeServer_pb2.EstimatedTimeRequest(atr=atra.tobytes(),num_atra=num_atr))
    ej = np.full((response.len,3),1)
    tiempos = np.frombuffer(response.times, dtype=ej.dtype).reshape(response.len,3)
    ponerTiemposEnMapa(tiempos)
    
    #print("Client received: " + response.times.decode('utf-8'))


def leerPosicionAtracciones():
    dir = os.path.join(os.path.dirname(__file__),'..','db.db')
    conn = create_connection(dir)
    c=conn.cursor()
    c.execute("""SELECT valor, x, y from mapa""")
    pos_atr=c.fetchall()

def ponerTiemposEnMapa(tiempos):
    global matriz
    global pos_atr

    for i in range(len(tiempos)):
        for j in range(len(pos_atr)):
            if tiempos[i][0]==pos_atr[j][0]:
                matriz[pos_atr[j][2]][[pos_atr[j][1]]]=tiempos[i][1]


#Funcion para conectarnos a la BD.
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
    atracciones = np.full((num_atr,3),'---')
    i=0
    for atr in mapa:
        c.execute("""SELECT * FROM atracciones where id='%s'""" %(atr[3]))
        query = c.fetchall()
        atracciones[i] = [query[0][0],query[0][1],query[0][2]]
        i+=1

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
    global num_atr
    for atr in mapa:
        x = atr[1]
        y = atr[2]
        matriz[x][y] = atr[3]
        num_atr+=1
    return matriz

#Funcion que crea la lista de atracciones
def crearListaAtr(atr):
    lista_atr=[]

    for i in range(num_atr):
        lista_atr.append(atr[i][0])
    return lista_atr

#Funcion que crea la cola de atracciones
def crearCola(lista_atr):
    mat = []
    for i in range (num_atr):
        rowList = []
        for j in range (1):
            rowList.append(lista_atr[j])
        mat.append(rowList)

    return mat 

#Funcion que esta a la escucha de los usuarios
def escuchaVisitante(server,puerto):
    consumer = KafkaConsumer(
        'movimiento',
        bootstrap_servers=['%s:%s'%(server,puerto)],
    )

    for msg in consumer:
        print(msg)
        datos=msg.value.decode('UTF-8').split(':')
        movimiento(datos[0],datos[1],datos[2])
        enviarMapa(server,puerto,datos[0])

#Funcion que envia el mapa actualizado al visitante
def enviarMapa(server,puerto,id_visitante):
    producer = KafkaProducer(bootstrap_servers=['%s:%s' %(server,puerto)])
    mensaje = matriz.tobytes()
    producer.send('%s' %(id_visitante), mensaje)
    producer.flush()

#Funcion que recibe las entradas de los visitantes
def entradaVisitante(server,puerto):
    consumer = KafkaConsumer(
        'loginAttempt',
        bootstrap_servers=['%s:%s'%(server,puerto)],
    )
    global visitantes_actual
    global cola_entrada
    global posiciones

    for msg in consumer:
        #print(msg)
        datos=msg.value.decode('UTF-8')

        if not cola_entrada:
            if visitantes_actual < int(visitantes_max):
                visitantes_actual+=1
                matriz[0][0] = datos
                posiciones = np.append(posiciones,[datos,0,0]).reshape(len(posiciones)+1,3)
                print("respuesta enviada")
                print(posiciones)
                respuestaEntradaVisitante(server,puerto,datos,True)
                
            else:
                cola_entrada.append(datos)
                respuestaEntradaVisitante(server,puerto,datos,False)
        else:
            cola_entrada.append(datos)
            respuestaEntradaVisitante(server,puerto,datos,False)

#Funcion que envia la respuesta al usuario que intenta entrar al parque
def respuestaEntradaVisitante(server,puerto,user,bool):
    if bool:
        respuesta = b'1'
    else:
        respuesta = b'0'
    print("Engine antes de send")
    producer = KafkaProducer(bootstrap_servers=['%s:%s' %(server,puerto)])
    producer.send('loginResponse.%s' %(user), respuesta)
    
    producer.flush()

    if bool:
        enviarMapa(server,puerto,user)

#Funcion que se ejecuta cada segundo para verificar si un usuario en cola puede entrar al parque
def colaParque(server,puerto):
    global visitantes_actual,posiciones
    delay = 1
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            if cola_entrada:
                if visitantes_actual < visitantes_max:
                    user = cola_entrada[0]
                    del cola_entrada[0]
                    posiciones = np.append(posiciones,[user,0,0]).reshape(len(posiciones)+1,3)
                    matriz[0][0] = user
                    visitantes_actual += 1
                    respuestaEntradaVisitante(server,puerto,user,True)

        except Exception:
            traceback.print_exc()
        next_time += delay

#Funcion que recibe las salidas de los visitantes
def salidaVisitante(server,puerto):
    consumer = KafkaConsumer(
        'logout',
        bootstrap_servers=['%s:%s'%(server,puerto)],
        )

    global visitantes_actual,posiciones

    for msg in consumer:
        user = msg.value.decode('UTF-8')
        borrarPos(user)
        visitantes_actual-=1

def borrarPos(id_user):
    global posiciones
    newMat=[]

    for i in range(0,len(posiciones)):
        if posiciones[i][0] == id_user:
            rem = posiciones[i]
        else:
            newMat = np.append(newMat,posiciones[i]).reshape(len(newMat)+1,3)
    posiciones = newMat

    return rem

#Funcion que registra el movimiento del usuario
def movimiento(usuario,x,y):
    global posiciones, matriz

    pos_ant = borrarPos(usuario)
    matriz[pos_ant[1]][pos_ant[2]]='---'
    posiciones = np.append(posiciones,[usuario,x,y]).reshape(len(posiciones)+1,3)
    

    if matriz[x][y] == '---':
        matriz[x][y] == usuario


#Funcion principal
def main():
    if(len(sys.argv) != 6):
        print("Para ejecutar utiliza: FWQ_Engine.py |IP GESTOR| |PUERTO GESTOR| |NUM MAX VISITANTES| |IP WaitingTimeServer| |PUERTO WaitingTimeServer|")
    else:
        global visitantes_max

        ip_gestor = sys.argv[1]
        puerto_gestor = sys.argv[2]
        visitantes_max = sys.argv[3]
        ip_wts = sys.argv[4]
        puerto_wts = sys.argv[5]

        #print(ObtenerTiempo(ip_wts,puerto_wts))

        #direccion de la BD
        #conn = create_connection('C:\\Users\\niktr\\Desktop\\SD-FWQ\\SD-FWQ\\db.db')

        dir = os.path.join(os.path.dirname(__file__),'..','db.db')
        conn = create_connection(dir)

        c=conn.cursor()

        id_mapa = 'm2'

        leerPosicionAtracciones() #Guardamos las posiciones de atracciones en la lista

        mapa = get_mapa(c,id_mapa)
        global matriz 
        matriz = rellenar_mapa(mapa)
        atr= get_atracciones(c,mapa)
        conn.close()

        lista_atr = crearListaAtr(atr)
        cola = crearCola(lista_atr)
        

        
        threading.Thread(target = entradaVisitante, args=(ip_gestor,puerto_gestor)).start()
        threading.Thread(target = colaParque, args=(ip_gestor,puerto_gestor)).start()
        threading.Thread(target = escuchaVisitante, args=(ip_gestor,puerto_gestor)).start()
        threading.Thread(target = salidaVisitante, args=(ip_gestor,puerto_gestor)).start()
        threading.Thread(target = reloj, args=(ip_wts,puerto_wts,atr)).start()


#------------------------
if __name__=="__main__":
    main() 