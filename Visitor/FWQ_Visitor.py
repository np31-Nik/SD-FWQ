from __future__ import print_function
from kafka import KafkaConsumer
from kafka import KafkaProducer
import numpy as np
from numpy import random
import logging
import grpc
import atexit
import sys
import time
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Registry'))
import Registry_pb2
import Registry_pb2_grpc

UserID = -1
matriz = Matriz = np.full((20,20), '---')
serverK = 0
puertoK = 0 
buscarAtr=False
atraccionActual=[-1,-1]
subir = False
#Funcion que envia el movimiento del usuario al engine, y luego imprime el mapa
def enviarPaso(fila,columna,server,puerto):
    producer = KafkaProducer(bootstrap_servers=['%s:%s' %(server,puerto)])
    mensaje = '%s:%s:%s' %(UserID,str(fila),str(columna))
    producer.send('movimiento', bytes(mensaje,'UTF-8'))
    producer.flush()
    producer.close()

def esperaCola(server,puerto,datos):
    global atraccionActual
    #atraccionActual=datos[1]
    print('Has entrado a la atraccion ',datos[1],', hay que esperar ',datos[2],' segundos.')
    time.sleep(int(datos[2]))

#Funcion que recibe el mapa desde engine
def recibirMapa(server,puerto):
    consumer = KafkaConsumer(
        '%s'%(UserID),
        group_id='RecibirMapa',
        bootstrap_servers=['%s:%s'%(server,puerto)],
        #enable_auto_commit=False
        )
    print('esperando mapa...')
    global matriz
    ej = np.full((20,20),'---')
    mapa=True
    global subir
    for msg in consumer:
        print('mapa recibido!')
        try:
            datos=msg.value.decode('UTF-8').split(':')
            if datos[0] == 'espera':
                esperaCola(server,puerto,datos)
                mapa=False
                subir = False
            else:
                mapa=True
        except:
            print('except')
            mapa=True
               
        if mapa:
            print('mapa asignado')
            matriz = np.frombuffer(msg.value, dtype=ej.dtype).reshape(20,20)
        break
    consumer.close()
    print_mapa(matriz)
    return mapa


#Funcion que imprime el mapa por consola
def print_mapa(matriz):

    print('Tu ID: ',UserID)
    for i in range(0,20):
        for j in range(0,20):
            print("\t{0}".format(matriz[i][j]),sep=',',end='')
        print('')

    print('')
    print('')

#Cuenta numero de atracciones y luego elige una random
def buscarAtraccion(): 
    contador =0 #Contador de atracciones
    for row in range(len(matriz)):
        for col in range(len(matriz[row])):
            if matriz[row][col]!='---' and matriz[row][col].find('u')==-1 and matriz[row][col]!='X':
                contador=contador+1
    encontrado=False
    global atraccionActual
    if contador!=0:
        while not encontrado:
            atraccion=random.randint(0,contador) #comprobar si funciona
            
            contador =0
            cerradas = 0
            for row in range(len(matriz)):
                for col in range(len(matriz[row])):
                    if matriz[row][col]!='---' and matriz[row][col].find('u')==-1 and matriz[row][col]!='X':
                        if contador==atraccion and row != atraccionActual[0] and col!=atraccionActual[1]:
                            #print('matriz[r][c]:',matriz[row][col],' atrAct:',atraccionActual) 
                            atraccionActual[0]=row
                            atraccionActual[1]=col
                            encontrado = True
                            return row,col
                        contador=contador+1
    else:
        return -1,-1


def moverse(server,port):
    fila=0
    columna=0
    booleano=True
    global subir
    while True:
        filaAtraccion=-1 
        colAtraccion=-1
        #print("Buscando atraccion")
        filaAtraccion,colAtraccion=buscarAtraccion()
        if filaAtraccion==-1 and colAtraccion==-1:
            print("Todo cerrado")
            enviarPaso(-1,-1,server,port)
            recibirMapa(server,port)
        else:
            print(filaAtraccion,colAtraccion)
            booleano=True
            #if filaAtraccion!=-1:
            #  booleano=False
            while booleano:
                time.sleep(1)

                if filaAtraccion==-1 and colAtraccion==-1:
                        print("Todo cerrado")
                        enviarPaso(-1,-1,server,port)
                        recibirMapa(server,port)
                        filaAtraccion,colAtraccion= buscarAtraccion()

                else:
                    fila,columna,booleano=calcularPaso(fila,columna,filaAtraccion,colAtraccion)
                    
                    #print('fA,cA',filaAtraccion,colAtraccion)
                    #print('f,c,b',fila,columna,booleano)
                    enviarPaso(fila,columna,server,port)
                    print('moviendome a:[',fila,',',columna,'], Atraccion:[',filaAtraccion,',',colAtraccion,']')
                    subir = True
                    recibirMapa(server,port)
                    booleano = subir
                    if matriz[filaAtraccion][colAtraccion]=='X':
                        print("SE HA CERRADO WEY :( que hace frio")
                        filaAtraccion,colAtraccion= buscarAtraccion()


    #----En bucle:
    #2) Esperar a recibir el mapa
    #3) comprobar tiempo de espera de una atraccion
    #4) Calcular el siguiente paso con funcion CalcularPaso
    #5) Enviar el paso cada segundo


def calcularPaso(fila,columna,filaAtraccion, colAtraccion):
    booleano=False

    if fila<filaAtraccion:
        fila=fila+1
        if matriz[fila][columna]=='X':
            #recalcular
            columna=columna+1
            print('recalculando ruta...')
        return fila,columna,False
    elif fila>filaAtraccion:
        fila=fila-1
        if matriz[fila][columna]=='X':
            #recalcular
            columna=columna+1
            print('recalculando ruta...')
        return fila,columna,False
    elif columna>colAtraccion:
        columna=columna-1
        if matriz[fila][columna]=='X':
            #recalcular
            fila=fila+1
            print('recalculando ruta...')
        return fila,columna,False
    elif columna<colAtraccion:
        columna=columna+1
        if matriz[fila][columna]=='X':
            #recalcular
            fila=fila+1
            print('recalculando ruta...')
        return fila,columna,False
    else:
        if fila==filaAtraccion and columna==colAtraccion:
            booleano=True
            return fila,columna,booleano

    # else:   
    #     if columna<colAtraccion and fila<filaAtraccion:
    #         columna=columna+1
    #         fila=fila+1
    #         return fila,columna
    #         #return 'NE' #North-East
    #     elif columna<colAtraccion and fila>filaAtraccion:
    #         columna=columna+1
    #         fila=fila-1
    #         return fila,columna
    #         #return 'SE' #South-East
    #     elif columna>colAtraccion and fila<filaAtraccion:
    #         columna=columna-1
    #         fila=fila+1
    #         return fila,columna
    #         #return 'NW' #North-West
    #     elif columna>colAtraccion and fila>filaAtraccion:
    #         columna=columna-1
    #         fila=fila-1
    #         return fila,columna
    #         #return 'SW' #South-West

    return (fila,columna,booleano)




def AskNamePassword():
    print("Introduzca el nombre de usuario:")
    username=input()
    print("Introduzca la contrasenya:")
    password=input()

    return username, password



def registarse(ip,puerto):
    channel = grpc.insecure_channel('%s:%s'%(ip,puerto))
    #channel = grpc.insecure_channel('localhost:50051')
    #channel = grpc.insecure_channel('192.168.4.246:50051')
    stub = Registry_pb2_grpc.RegistryServiceStub(channel)
    name,password=AskNamePassword()
    #response = stub.Registry(Registry_pb2.RegistryRequest(ID=1,name="you",password="12345"))
    response = stub.Registry(Registry_pb2.RegistryRequest(ID=1,name=name,password=password))
    print(response.response)


def iniciarSesion(ip,puerto,usr=-1,pwd=-1):
    global UserID
    channel = grpc.insecure_channel('%s:%s'%(ip,puerto))
    #channel = grpc.insecure_channel('localhost:50051')
    #channel = grpc.insecure_channel('192.168.4.246:50051')
    stub = Registry_pb2_grpc.loginStub(channel)
    if usr!=-1:
        username,password=(usr,pwd)
    else:
        username,password=AskNamePassword()
    response = stub.Login(Registry_pb2.loginRequest(username=username,password=password))
    print(response.response)
    if response.response!="El nombre de usuario o la contraseña no son correctos":
        UserID=response.response
        return True
    else:
        return False


def modificarUsuario(ip,puerto):
    channel = grpc.insecure_channel('%s:%s'%(ip,puerto))
    channel = grpc.insecure_channel('localhost:50051')
    #channel = grpc.insecure_channel('192.168.4.246:50051')
    stub = Registry_pb2_grpc.modifyUserStub(channel)
    username,password=AskNamePassword()
    print("Introduzca nuevo nombre de usuario o deje vacio si solo quiere cambiar la contrasenya")
    newUsername=input()
    if newUsername=='':
        newUsername=username
    print("Introduzca la nueva contrasenya o deje vacio si solo quiere cambiar el nombre de usuario")
    newPassword=input()
    if newPassword=='':
        newPassword=password
    response = stub.Modify(Registry_pb2.changeUserInfo
        (username=username,password=password,newUsername=newUsername,newPassword=newPassword))
    #response = stub.Modify(Registry_pb2.changeUserInfo
    #    (username="alfonsox1",password="12346",newUsername="alfonsox1",newPassword="12345"))
    print(response.response)
    return response.response


def enviaEntradaParque(server,puerto):
    producer = KafkaProducer(bootstrap_servers=['%s:%s' %(server,puerto)])
    id=bytes(UserID, 'utf-8')
    producer.send('loginAttempt', id)
    producer.flush()
    producer.close()
    #print("Entrada enviada")
    


def recibeEntradaParque(server,puerto):
    consumer = KafkaConsumer(
        'loginResponseX%s'%(UserID),
        group_id='login',
        bootstrap_servers=['%s:%s'%(server,puerto)],
        #enable_auto_commit=False

        )
    #print("Entrada recibida de Engine")
    print('userID:',UserID)
    for msg in consumer:
        datos = msg.value.decode('UTF-8')
        if datos == '1':    
            print('Has entrado al parque.')
            break
        elif datos == '0':
            print('Hay una cola para entrar al parque, espera tu turno...')
        elif datos == '-1':
            print('Este usuario ya esta en linea.')
        else:
            print('Error en recibeEntradaParque()')

   # print("Despues de for")
    consumer.close()
    
def login(serverGrpc,puertoGrpc,serverKafka,puertoKafka,usr=-1,pwd=-1):
    if iniciarSesion(serverGrpc,puertoGrpc,usr,pwd):
                    enviaEntradaParque(serverKafka,puertoKafka)
                    recibeEntradaParque(serverKafka,puertoKafka)
                    recibirMapa(serverKafka,puertoKafka)
                    moverse(serverKafka,puertoKafka)

#Funcion principal
def run():
    if(len(sys.argv)==7):
            serverGrpc = sys.argv[1]
            puertoGrpc = sys.argv[2]
            serverKafka = sys.argv[3]
            puertoKafka=sys.argv[4]
            usr = sys.argv[5]
            pwd = sys.argv[6]
            login(serverGrpc,puertoGrpc,serverKafka,puertoKafka,usr,pwd)
    elif(len(sys.argv) != 5):
        print("Para ejecutar utiliza: FWQ_Sensor.py |IP GRPC SERVER| |PUERTO| |IP BROKER SERVER| |PUERTO|")
    else:
        serverGrpc = sys.argv[1]
        puertoGrpc = sys.argv[2]
        serverKafka = sys.argv[3]
        puertoKafka=sys.argv[4]

        global UserID
        global serverK
        global puertoK
        global matriz

        serverK = serverKafka
        puertoK = puertoKafka
        UserID="-1"

        opcion=0
        while True:
            print("Eliga una opcion: \n 1) Registrarse; \n 2) Iniciar sesion y entrar al parque; \n 3) Modificar usuario; \n 4) Salir;")
            opcion = input()
            if opcion == "1":
                registarse(serverGrpc,puertoGrpc)
            if opcion == "2":
                login(serverGrpc,puertoGrpc,serverKafka,puertoKafka)                
            if opcion == "3":
                modificarUsuario(serverGrpc,puertoGrpc)
            if opcion =="4":
                handle_exit()
                break
        
        


import signal

#Funcion que se ejecuta al salir del programa
def handle_exit(one,two):
    #print(serverK,puertoK)
    producer = KafkaProducer(bootstrap_servers=['%s:%s' %(serverK,puertoK)])
    mensaje = bytes('%s' %(UserID),'UTF-8')
    print('Saliendo...')
    producer.send('logout', mensaje)
    producer.flush()
    producer.close()

atexit.register(handle_exit,'1','2')
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

if __name__ == "__main__":
    logging.basicConfig()
    run()
