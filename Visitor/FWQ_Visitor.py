from __future__ import print_function
from kafka import KafkaConsumer
from kafka import KafkaProducer
import logging

import grpc

import atexit
import numpy as np
import sys

sys.path.append('C:/Users/serg2/source/repos/SD-FWQ/Registry')
import Registry_pb2
import Registry_pb2_grpc


def AskNamePassword():
    print("Introduzca el nombre de usuario:")
    username=input()
    print("Introduzca la contrasenya:")
    password=input()

    return username, password


def registarse():
    channel = grpc.insecure_channel('localhost:50051')
    #channel = grpc.insecure_channel('192.168.4.246:50051')
    stub = Registry_pb2_grpc.RegistryServiceStub(channel)
    name,password=usernamePassword()
    #response = stub.Registry(Registry_pb2.RegistryRequest(ID=1,name="you",password="12345"))
    response = stub.Registry(Registry_pb2.RegistryRequest(ID=1,name=name,password=password))
    print("Client received: " + response.response)


def iniciarSesion():
    channel = grpc.insecure_channel('localhost:50051')
    #channel = grpc.insecure_channel('192.168.4.246:50051')
    stub = Registry_pb2_grpc.loginStub(channel)
    username,password=AskNamePassword()
    response = stub.Login(Registry_pb2.loginRequest(username=username,password=password))
    #response = stub.Login(Registry_pb2.loginRequest(username="alfonsox1",password="12345"))
    print("Client received: " + response.response)

    #Continuacio:
    #1) Esperar a recibir el mapa
    #2) Elegir atraccion
    #----En bucle:
    #3) comprobar tiempo de espera de una atraccion
    #4) Calcular el siguiente paso con funcion CalcularPaso
    #5) Enviar el paso cada segundo
    

    
def modificarUsuario():
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

def calcularPaso(fila,columna,filaAtraccion, colAtraccion):
    if fila==filaAtraccion:
        if columna<colAtraccion:
            columna=columna+1
        else:
            columna=columna-1

    if columna==colAtraccion:
        if fila<filaAtraccion:
            fila=fila+1
        else:
            fila=fila-1
    else:
        if columna<colAtraccion and fila<filaAtraccion:
            columna=columna+1
            fila=fila+1
        elif columna<colAtraccion and fila>filaAtraccion:
            columna=columna+1
            fila=fila-1
        elif columna>colAtraccion and fila<filaAtraccion:
            columna=columna-1
            fila=fila+1
        elif columna>colAtraccion and fila>filaAtraccion:
            columna=columna-1
            fila=fila-1


def enviarPaso(id,server,puerto):
    
    global personas
    consumer = KafkaConsumer(
        '%s' %(id),
        bootstrap_servers=['%s:%s'%(server,puerto)],
    )

    for msg in consumer:
        print(msg)


@atexit.register
#HACER QUE DESAPAREZCA O SE DESCONECTE DE ENGINE AL SALIR
def goodbye():
    print('You are now leaving the Python sector.')

def run():
    if False:
    #if(len(sys.argv) != 5):
        print("Para ejecutar utiliza: FWQ_Sensor.py |IP GRPC SERVER| |PUERTO| |IP BROCKER SERVER| |PUERTO|")
    else:
        # serverGrpc = sys.argv[1]
        # puertoGrpc = sys.argv[2]
        # serverKafka = sys.argv[3]
        # puertoKafa=sys.argv[4]

        # fila=0
        # columna=0

        #Lo que falta por hacer:
        #
        #Elige al azar una de las atracciones con menos de 60 minutos de espera y va hacia ella
        #Si en el camino cambia a tener 60 minuos o mas elige otra.
        #Cada segundo dara un paso en una de la 8 direcciones
        #LLamar desde iniciar sesion a una funcion que haga pasos en bucle

        matriz = np.full((20,20), '---')
        matriz[2][2]='a1'
        matriz[4][9]='a2'
        matriz[13][18]='a3'
        matriz[5][1]='a4'
        matriz[8][8]='a5'
        print(matriz)

        opcion=0
        while(opcion!=1 or opcion!= 2 or opcion!=3):
            print("Eliga una opcion: \n 1) Registrarse; \n 2) Iniciar sesion y entrar al parque; \n 3) Modificar usuario;\n 4) Salir;")
            opcion = input()
            if opcion == "1":
                registarse()
            if opcion == "2":
                iniciarSesion()
            if opcion == "3":
                modificarUsuario()
            if opcion =="4":
                break
        
        print("Hasta pronto!")

if __name__ == "__main__":
    logging.basicConfig()
    run()
