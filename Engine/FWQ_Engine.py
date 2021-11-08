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
serverK = 0
puertoK = 0

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
    error = -1
    try:
        #channel = grpc.insecure_channel('localhost:50051')
        channel = grpc.insecure_channel('%s:%s' %(ip,port))
        stub = TimeServer_pb2_grpc.CalculateTimeStub(channel)
        #print(atra)
        response = stub.Time(TimeServer_pb2.EstimatedTimeRequest(atr=atra.tobytes(),num_atra=num_atr))
        ej = np.full((response.len,2),'---')
        #print('response.len:',response.len)
        tiempos = np.frombuffer(response.times, dtype=ej.dtype)
        #print('tiempos:',tiempos)
        tiempos = tiempos.reshape(response.len,2)
        #print('actualizando tiempos:',tiempos)
        ponerTiemposEnMapa(tiempos)
        #print_mapa()
        
        #print("Client received: " + response.times.decode('utf-8'))
    except:
        error += 1    


def leerPosicionAtracciones():
    dir = os.path.join(os.path.dirname(__file__),'..','db.db')
    conn = create_connection(dir)
    c=conn.cursor()
    c.execute("""SELECT valor, x, y from mapa""")
    pos_atr=c.fetchall()
    print('pos_atr:',pos_atr)

def ponerTiemposEnMapa(tiempos):
    global matriz
    global pos_atr
    print('poniendo tiempos en el mapa')
    for i in range(len(tiempos)):
        for j in range(len(pos_atr)):
            if tiempos[i][0]==pos_atr[j][0]:
                print('cambio en matriz (tiempo)')
                matriz[pos_atr[j][1]][[pos_atr[j][2]]]=tiempos[i][1]


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
def print_mapa():

    for i in range(0,20):
        for j in range(0,20):
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
        print('movimiento recibido:',datos)
        movimiento(datos[0],datos[1],datos[2])
        enviarMapa(server,puerto,datos[0])

#Funcion que envia el mapa actualizado al visitante
def enviarMapa(server,puerto,id_visitante):
    print('enviando mapa...')
    producer = KafkaProducer(bootstrap_servers=['%s:%s' %(server,puerto)])
    mensaje = matriz.tobytes()
    print_mapa()
    producer.send('%s' %(id_visitante), mensaje)
    producer.flush()
    print('mapa enviado!')

#Funcion que recibe las entradas de los visitantes
def entradaVisitante(server,puerto):
    consumer = KafkaConsumer(
        'loginAttempt',
        bootstrap_servers=['%s:%s'%(server,puerto)],
    )
    global visitantes_actual
    global cola_entrada
    global posiciones
    global matriz

    for msg in consumer:
        #print(msg)
        datos=msg.value.decode('UTF-8')
        print('usuario ha entrado: ',datos)
        repetido=False
        if not cola_entrada:
            if visitantes_actual < visitantes_max:
                for i in range(0,visitantes_actual):
                    if posiciones[i][0] == datos:
                        respuestaEntradaVisitante(server,puerto,datos,-1)
                        repetido = True

                if not repetido:
                    visitantes_actual+=1
                    matriz[0][0] = datos
                    
                    posiciones = np.append(posiciones,[datos,0,0]).reshape(len(posiciones)+1,3)
                    print("respuesta enviada")
                    print_mapa()                    
                    print(posiciones)
                    respuestaEntradaVisitante(server,puerto,datos,1)
                
            else:
                cola_entrada.append(datos)
                respuestaEntradaVisitante(server,puerto,datos,0)
        else:
            cola_entrada.append(datos)
            respuestaEntradaVisitante(server,puerto,datos,0)

#Funcion que envia la respuesta al usuario que intenta entrar al parque
def respuestaEntradaVisitante(server,puerto,user,resp):
    resp = bytes(str(resp),'utf-8')
    print("Engine antes de send")
    producer = KafkaProducer(bootstrap_servers=['%s:%s' %(server,puerto)])
    print('user: ',user, ' resp:',resp)
    producer.send('loginResponse.%s' %(user), resp)
    
    producer.flush()

    if bool:
        print('mapa de entrada')
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
        print('alguien ha salido')
        user = msg.value.decode('UTF-8')
        borrarPos(user)
        visitantes_actual-=1

def borrarPos(id_user):
    global posiciones
    newMat=[]
    rem=[]

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
    #print('usuario:?',usuario)
    #print('usuario se mueve:',usuario)
    pos_ant = borrarPos(usuario)
    #print('pos_ant:?',pos_ant)
    print('x:',int(x),' y:',int(y),' mat[x][y]:', matriz[int(x)][int(y)],' usuario:', usuario)

    if matriz[int(pos_ant[1])][int(pos_ant[2])]==usuario:
        matriz[int(pos_ant[1])][int(pos_ant[2])]='---'
        #print('borra pos anterior a ---')
    posiciones = np.append(posiciones,[usuario,x,y]).reshape(len(posiciones)+1,3)
    #print('x:? \ y:?',x,y)

    if matriz[int(x)][int(y)] == '---':
        matriz[int(x)][int(y)] = usuario
    elif matriz[int(x)][int(y)].startswith('u'):
        print('misma pos que otro usuario')
    else:
        atr_id = obtenerIDatr(int(x),int(y))
        print('Entrando a la atraccion')
        enviarSensor(atr_id,usuario)
        #print('cambio de matriz')
        #print_mapa()

def enviarSensor(id_atr,id_user):
    producer = KafkaProducer(bootstrap_servers=['%s:%s' %(serverK,puertoK)])
    print('Enviando mensaje a sensor:',id_atr)
    mensaje = bytes(id_user,'utf-8')
    producer.send('%s' %(id_atr), mensaje)
    producer.flush()

def obtenerIDatr(x,y):
    id = -1
    for i in len(pos_atr):
        if pos_atr[i][1]==x and pos_atr[i][2]==y:
            id = pos_atr[i][0]
            break
    return id

#Funcion principal
def main():
    if(len(sys.argv) != 6):
        print("Para ejecutar utiliza: FWQ_Engine.py |IP GESTOR| |PUERTO GESTOR| |NUM MAX VISITANTES| |IP WaitingTimeServer| |PUERTO WaitingTimeServer|")
    else:
        global visitantes_max

        ip_gestor = sys.argv[1]
        puerto_gestor = sys.argv[2]
        visitantes_max = int(sys.argv[3])
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
        print_mapa()
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