from kafka import KafkaConsumer
from kafka import KafkaProducer
import time
import sqlite3
import numpy as np
import sys
from concurrent import futures
import logging
import grpc
import random

import os

from six import print_
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
serverK = "0"
puertoK = "0"
tiempos = []
#clima:
temp_threshold= (20,30)
ciudades = []
ciudades_old = []

# importing requests and json
import requests, json

def leerUsuariosOnline():
    print("leyendo fichero")
    archivo = "../Registry/usersOnline.txt"
    f= open(archivo,'r')

    lines = f.readlines()
    
    for i in range(len(lines)):
        online=False
        for p in range(len(posiciones)):
            if lines[i] in posiciones[p]:
                online=True
                break
        if not online:
            print("not online")
    

def reloj2():
#print("reloj")
    delay = 1
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            if obtenerClima():
                print_mapa()

        except Exception:
            traceback.print_exc()
        next_time += delay

def actualizarCiudades():
    global ciudades_old
    archivo = "ciudades.txt"
    f= open(archivo,'r')

    r = f.read()
    r = r.split(',')
    c=[]

    if ciudades_old != r:
        i = 0
        while i < 4:
            rand = random.randint(0,len(r)-1)
            if r[rand] not in c:
                c.append(r[rand])
                i += 1
        ciudades_old = r
    else:
        c=ciudades

    f.close()

    return c

def climaAtracciones(t,c):
    print("Cambiando estado de atracciones por el clima...")

    rangoX = (0,0)
    rangoY = (0,0)

    if c == 0:
        rangoX = (0,10)
        rangoY = (0,10)
    elif c == 1:
        rangoX = (10,20)
        rangoY = (0,10)
    elif c == 2:
        rangoX = (0,10)
        rangoY = (10,20)
    else:
        rangoX = (10,20)
        rangoY = (10,20)

    for i in range(len(pos_atr)):
        x = int(pos_atr[i][1])
        y = int(pos_atr[i][2])
        if (x > rangoX[0] and x < rangoX[1]) and (y > rangoY[0] and y < rangoY[1]):
            if t < 20 or t > 30:
                matriz[x][y] = 'X'
            else:
                matriz[x][y] = pos_atr[i][0]
                
    

# Funcion que obtiene el clima de las 4 ciudades
def obtenerClima():

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    API_KEY = "291383717ab69005393ff7fd27b2605a"
    global ciudades
    c = actualizarCiudades() # Lista de ciudades leida del fichero

    if c != ciudades:
        ciudades=c
        for i in range(len(ciudades)):
            CITY = ciudades[i]
            URL = BASE_URL + "q=" + CITY + "&units=metric"+ "&appid=" + API_KEY
            response = requests.get(URL)
            
            if response.status_code == 200:
                data = response.json()
                main = data['main']
                temperature = main['temp']
                print(f"{CITY:-^30}")
                print(f"Temperature: {temperature}")

                climaAtracciones(temperature,i) # Se actualiza el mapa acorde al clima
            else:
                print("Error in the HTTP request")
                return False
        return True
    else:
        # Sin cambios:
        return False

#Escribir en fichero
def escribirFichero():
    
    archivo = "mapaTemp.txt"
    f= open(archivo,'w')
    f.write('Mapa: <br>')

    original_stdout = sys.stdout # Save a reference to the original standard output
    sys.stdout = f # Change the standard output to the file we created.

    for i in range(0,20):
        for j in range(0,20):
            print("\t{0}".format(matriz[i][j]),sep=',',end='')
        print('<br>')

    sys.stdout = original_stdout # Reset the standard output to its original value

    f.close()


    archivo2 = "usuariosTemp.txt"
    f2= open(archivo2,'w')
    f2.write('Usuarios: <br>')

    for i in range(0,len(posiciones)):
        if posiciones[i][0]!='---':
            f2.write(str(posiciones[i]))
            f2.write('<br>')
    f2.close()


def reloj(ip,puerto,atr):
	#print("reloj")
	delay = 2
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
    error = 0
    global tiempos
    try:
        #print('obteniendo tiempos')
        #channel = grpc.insecure_channel('localhost:50051')
        channel = grpc.insecure_channel('%s:%s' %(ip,port))
        stub = TimeServer_pb2_grpc.CalculateTimeStub(channel)
        #print(atra)
        response = stub.Time(TimeServer_pb2.EstimatedTimeRequest(atr=atra.tobytes(),num_atra=num_atr))
        ej = np.full((response.len,2),'---')
                #print('obteniendo tiempos')

        #print('response.len:',response.len)
        tiempos = np.frombuffer(response.times, dtype=ej.dtype)
        #print('tiempos:',tiempos)
        tiempos = tiempos.reshape(response.len,2)
        #print('actualizando tiempos:',tiempos)
        ponerTiemposEnMapa()
        #print_mapa()
        
        #print("Client received: " + response.times.decode('utf-8'))
    except:
        error += 1    


def leerPosicionAtracciones(id_mapa):
    dir = os.path.join(os.path.dirname(__file__),'..','db.db')
    conn = create_connection(dir)
    c=conn.cursor()
    c.execute("""SELECT valor, x, y from mapa where id='%s'""" %(id_mapa))
    query=c.fetchall()
    conn.close()
    global pos_atr
    resultado_matriz = np.full((num_atr,3),'---')

    for i in range(num_atr):
        resultado_matriz[i]=[query[i][0],query[i][1],query[i][2]]
    pos_atr = resultado_matriz
    #print('pos_atr:',pos_atr)

def ponerTiemposEnMapa():
    global matriz
    global pos_atr
    global tiempos
    #print('poniendo tiempos en el mapa')
    #print(tiempos)
    for i in range(len(tiempos)):
        id_tiempo = tiempos[i][0]
        tiempo = tiempos[i][1]
        for j in range(len(pos_atr)):
            id_pos = pos_atr[j][0]
            x = int(pos_atr[j][1])
            y = int(pos_atr[j][2])
            if id_tiempo == id_pos:
                #print('cambio en matriz (tiempos)')
                if matriz[x][y]!='X':
                    matriz[x][y]=tiempo
                #print('matriz[x][y]:',matriz[x][y],' tiempo:',tiempo,' id_t:',id_tiempo,' id_pos:',id_pos)
            


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

    escribirFichero()

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
            rowList.append(lista_atr[i])
        mat.append(rowList)

    #print('mat:',mat)
    return mat 

#Funcion que esta a la escucha de los usuarios
def escuchaVisitante(server,puerto):
    consumer = KafkaConsumer(
        'movimiento',
        bootstrap_servers=['%s:%s'%(server,puerto)]
    )

    for msg in consumer:
        #print(msg)
        datos=msg.value.decode('UTF-8').split(':')
        print('movimiento recibido:',datos)
        enviar = movimiento(datos[0],datos[1],datos[2])
        if enviar:
            enviarMapa(server,puerto,datos[0])

#Funcion que envia el mapa actualizado al visitante
def enviarMapa(server,puerto,id_visitante):
    print('enviando mapa...')
    producer = KafkaProducer(bootstrap_servers=['%s:%s' %(server,puerto)])
    mensaje = matriz.tobytes()
    print_mapa()
    time.sleep(1)
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
                    
                    posiciones = np.append(posiciones,[datos,'0','0']).reshape(len(posiciones)+1,3)
                   # print('posiciones:',posiciones)
                   # print("respuesta enviada")
                    respuestaEntradaVisitante(server,puerto,datos,1)
                    #posiciones = np.append(posiciones,[datos,'0','0']).reshape(len(posiciones)+1,3)

                
            else:
                cola_entrada.append(datos)
                respuestaEntradaVisitante(server,puerto,datos,0)
        else:
            cola_entrada.append(datos)
            respuestaEntradaVisitante(server,puerto,datos,0)

#Funcion que envia la respuesta al usuario que intenta entrar al parque
def respuestaEntradaVisitante(server,puerto,user,resp):
    global posiciones
    mensaje = bytes(str(resp),'utf-8')
    #print("Engine antes de send")
    producer = KafkaProducer(bootstrap_servers=['%s:%s' %(server,puerto)])
    #print('user: ',user, ' resp:',resp)
    time.sleep(1)
    producer.send('loginResponseX%s' %(user),mensaje)
    
    producer.flush()

    if resp==1:

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
                    posiciones = np.append(posiciones,[user,'0','0']).reshape(len(posiciones)+1,3)
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
        print('Alguien ha salido.')
        user = msg.value.decode('UTF-8')
        borrarPos(user)
        visitantes_actual-=1

def borrarPos(id_user):
    global posiciones
    newMat=[]
    rem=[]
    #print('posicionesantes:',posiciones)

    for i in range(0,len(posiciones)):
        if posiciones[i][0] == id_user:
            rem = posiciones[i]
            x=int(rem[1])
            y=int(rem[2])
            matriz[x][y]='---'
        else:
            newMat = np.append(newMat,posiciones[i]).reshape(len(newMat)+1,3)
    posiciones = newMat
    #print('posiciones:',posiciones)

    return rem

def enviarEsperaVisitante(usuario,id_atr,tiempo):
    print('El usuario ',usuario,' debe esperar ',tiempo,'s')
    producer = KafkaProducer(bootstrap_servers=['%s:%s' %(serverK,puertoK)])
    mensaje = bytes('espera:%s:%s'%(id_atr,tiempo),'UTF-8')
    producer.send('%s' %(usuario), mensaje)
    producer.flush()



#Funcion que registra el movimiento del usuario
def movimiento(usuario,x,y):
    enviar_mapa=True
    global posiciones, matriz
    eliminado=True
    #print('usuario:?',usuario)
    #print('usuario se mueve:',usuario)
    
    #print('pos_ant:?',pos_ant)
    #print('x:',int(x),' y:',int(y),' mat[x][y]:', matriz[int(x)][int(y)],' usuario:', usuario)
    #print('movimiento posiciones',posiciones)
    if int(x)!= -1 and int(y)!=-1:
        for u in posiciones:
            #print('u0',u[0],' user:',usuario)
            if u[0]==usuario:
                eliminado=False
                #print('elim False')
        if not eliminado:
            pos_ant = borrarPos(usuario)
            #print('if not')
            if matriz[int(pos_ant[1])][int(pos_ant[2])]==usuario:
                matriz[int(pos_ant[1])][int(pos_ant[2])]='---'
                #print('borra pos anterior a ---')
            posiciones = np.append(posiciones,[usuario,x,y]).reshape(len(posiciones)+1,3)
            #print('x:? \ y:?',x,y)

            if matriz[int(x)][int(y)] == '---':
                matriz[int(x)][int(y)] = usuario
            elif matriz[int(x)][int(y)].startswith('u'):
                solapado=True
            else:
                atr_id = obtenerIDatr(x,y)
                #print('Entrando a la atraccion')
                enviarSensor(atr_id,usuario)
                where = np.where(tiempos[:,0]==atr_id)
                tiempo = tiempos[where][0][1]
                #print('tiempo|',tiempo)
                enviarEsperaVisitante(usuario,atr_id,tiempo)
                enviar_mapa=False
                #print('cambio de matriz')
                #print_mapa()
        else:
            enviar_mapa=False
    return enviar_mapa

def enviarSensor(id_atr,id_user):
    #print('Enviando mensaje a sensor:',id_atr,' serverK:',serverK,' puertoK:',puertoK,' id_user:',id_user)

    producer = KafkaProducer(bootstrap_servers=['%s:%s' %(serverK,puertoK)])
    mensaje = bytes(id_user,'utf-8')
    producer.send('%s' %(id_atr), mensaje)
    producer.flush()

def obtenerIDatr(x,y):
    id = -1
    #print('x:',x,' y:',y)
    for i in range(len(pos_atr)):
        #print('pos_atr[',i,']: ',pos_atr[i])
        if pos_atr[i][1]==x and pos_atr[i][2]==y:
            id = pos_atr[i][0]
            #print('ID ENCONTRADO')
            break
    #print('obtenerIDatr:',id)
    return id

#Funcion principal
def main():
    if(len(sys.argv) != 6):
        print("Para ejecutar utiliza: FWQ_Engine.py |IP GESTOR| |PUERTO GESTOR| |NUM MAX VISITANTES| |IP WaitingTimeServer| |PUERTO WaitingTimeServer|")
    else:
        global visitantes_max,serverK,puertoK

        serverK = ip_gestor = sys.argv[1]
        puertoK = puerto_gestor = sys.argv[2]
        visitantes_max = int(sys.argv[3])
        ip_wts = sys.argv[4]
        puerto_wts = sys.argv[5]

        #print(ObtenerTiempo(ip_wts,puerto_wts))

        #direccion de la BD
        #conn = create_connection('C:\\Users\\niktr\\Desktop\\SD-FWQ\\SD-FWQ\\db.db')

        dir = os.path.join(os.path.dirname(__file__),'..','db.db')
        conn = create_connection(dir)

        c=conn.cursor()

        id_mapa = 'm3'
        mapa = get_mapa(c,id_mapa)
        global matriz 
        matriz = rellenar_mapa(mapa)

        print_mapa()


        leerPosicionAtracciones(id_mapa) #Guardamos las posiciones de atracciones en la lista

        if obtenerClima():
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
        threading.Thread(target = reloj2).start()


#------------------------
if __name__=="__main__":
    main() 