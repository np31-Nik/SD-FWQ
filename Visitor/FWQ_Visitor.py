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

#Funcion que envia el movimiento del usuario al engine, y luego imprime el mapa
def enviarPaso(fila,columna,server,puerto):
    producer = KafkaProducer(bootstrap_servers=['%s:%s' %(server,puerto)])
    mensaje = '%s:%s:%s' %(UserID,str(fila),str(columna))
    producer.send('movimiento', bytes(mensaje,'UTF-8'))
    producer.flush()
    producer.close()


#Funcion que recibe el mapa desde engine
def recibirMapa(server,puerto):
    consumer = KafkaConsumer(
        '%s'%(UserID),
        group_id='RecibirMapa',
        bootstrap_servers=['%s:%s'%(server,puerto)],
        )
    print('esperando mapa...')
    global matriz
    ej = np.full((20,20),'---')

    for msg in consumer:
        print('mapa recibido!')
        matriz = np.frombuffer(msg.value, dtype=ej.dtype).reshape(20,20)
        break
    print('salimos del for (recibirMapa)')
    consumer.close()
    print_mapa(matriz)


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
            if matriz[row][col]!='---' and not matriz[row][col].startswith('u'):
                contador=contador+1
    print("Matriz de Buscar Atraccion")
    print(matriz)
    atraccion=random.randint(contador) #comprobar si funciona
    print(atraccion)
    contador =0
    for row in range(len(matriz)):
        for col in range(len(matriz[row])):
            if matriz[row][col]!='---':
                
                if contador==atraccion: 
                    return row,col
                contador=contador+1


def moverse(server,port):
    
    fila=0
    columna=0
    filaAtraccion=-1 
    colAtraccion=-1
    while filaAtraccion==-1:
            print("Buscando atraccion")
            (filaAtraccion,colAtraccion)=buscarAtraccion()
    while(True):
        (fila,columna)=calcularPaso(fila,columna,filaAtraccion,colAtraccion)
        enviarPaso(fila,columna,server,port)
        recibirMapa(server,port)
        #print_mapa(matriz)


    #----En bucle:
    #2) Esperar a recibir el mapa
    #3) comprobar tiempo de espera de una atraccion
    #4) Calcular el siguiente paso con funcion CalcularPaso
    #5) Enviar el paso cada segundo


def calcularPaso(fila,columna,filaAtraccion, colAtraccion):
    if fila==filaAtraccion:
        if columna<colAtraccion:
            columna=columna+1
            #return 'E' #East
        else:
            columna=columna-1
            #return 'W' #West

    if columna==colAtraccion:
        if fila<filaAtraccion:
            fila=fila+1
            #return 'N' #North
        else:
            fila=fila-1
            #return 'S' #South

    else:   
        if columna<colAtraccion and fila<filaAtraccion:
            columna=columna+1
            fila=fila+1
            #return 'NE' #North-East
        elif columna<colAtraccion and fila>filaAtraccion:
            columna=columna+1
            fila=fila-1
            #return 'SE' #South-East
        elif columna>colAtraccion and fila<filaAtraccion:
            columna=columna-1
            fila=fila+1
            #return 'NW' #North-West
        elif columna>colAtraccion and fila>filaAtraccion:
            columna=columna-1
            fila=fila-1
            #return 'SW' #South-West

    return (fila,columna)




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
    print("Client received: " + response.response)


def iniciarSesion(ip,puerto):
    global UserID
    channel = grpc.insecure_channel('%s:%s'%(ip,puerto))
    #channel = grpc.insecure_channel('localhost:50051')
    #channel = grpc.insecure_channel('192.168.4.246:50051')
    stub = Registry_pb2_grpc.loginStub(channel)
    username,password=AskNamePassword()
    response = stub.Login(Registry_pb2.loginRequest(username=username,password=password))
    print("Client received: " + response.response)
    if response.response!="El nombre de usuario o la contraseña no son correctos":
        UserID=response.response
        return True
    else:
        #print(response.response)
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
    print("Client received: " + response.response)
    return response.response


def enviaEntradaParque(server,puerto):
    producer = KafkaProducer(bootstrap_servers=['%s:%s' %(server,puerto)])
    id=bytes(UserID, 'utf-8')
    producer.send('loginAttempt', id)
    producer.flush()
    producer.close()
    print("Entrada enviada")
    


def recibeEntradaParque(server,puerto):
    consumer = KafkaConsumer(
        'loginResponse.%s'%(UserID),
        group_id='login',
        bootstrap_servers=['%s:%s'%(server,puerto)],
        )
    print("Entrada recibida de Engine")
    print('user:?',UserID)
    for msg in consumer:
        print("bucle")
        datos = msg.value.decode('UTF-8')
        print('resp:',datos)
        if datos == '1':    
            print('Has entrado al parque.')
            break
        elif datos == '0':
            print('Hay una cola para entrar al parque, espera tu turno...')
        elif datos == '-1':
            print('Este usuario ya esta en linea.')
        else:
            print('Error en recibeEntradaParque()')

    print("Despues de for")
    consumer.close()
    

#Funcion principal
def run():
    if(len(sys.argv) != 5):
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

        matriz[2][2]='a1'
        matriz[4][9]='a2'
        matriz[13][18]='a3'
        matriz[5][1]='a4'
        matriz[8][8]='a5'
        #print(matriz)

        opcion=0
        while True:
            print("Eliga una opcion: \n 1) Registrarse; \n 2) Iniciar sesion y entrar al parque; \n 3) Modificar usuario;\n 4) Salir;")
            opcion = input()
            if opcion == "1":
                registarse(serverGrpc,puertoGrpc)
            if opcion == "2":
                if iniciarSesion(serverGrpc,puertoGrpc):
                    enviaEntradaParque(serverKafka,puertoKafka)
                    recibeEntradaParque(serverKafka,puertoKafka)
                    recibirMapa(serverKafka,puertoKafka)
                    moverse(serverKafka,puertoKafka)
                
            if opcion == "3":
                modificarUsuario(serverGrpc,puertoGrpc)
            if opcion =="4":
                handle_exit()
                break
        
        


import signal
#Funcion que se ejecuta al salir del programa
def handle_exit():
    producer = KafkaProducer(bootstrap_servers=['%s:%s' %(serverK,puertoK)])
    mensaje = '%s' %(UserID)
    producer.send('logout', mensaje)
    producer.flush()
    producer.close()
atexit.register(handle_exit)
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

if __name__ == "__main__":
    logging.basicConfig()
    run()
