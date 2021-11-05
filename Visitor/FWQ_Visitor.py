from __future__ import print_function

import logging

import grpc

import atexit
import numpy as np
import sys
sys.path.append('C:/Users/serge/source/repos/SD-FWQ/Registry')
import Registry_pb2
import Registry_pb2_grpc


def registarse():
    channel = grpc.insecure_channel('localhost:50051')
    #channel = grpc.insecure_channel('192.168.4.246:50051')
    stub = Registry_pb2_grpc.RegistryServiceStub(channel)
    response = stub.Registry(Registry_pb2.RegistryRequest(ID=1,name="you",password="12345"))
    print("Client received: " + response.response)


def iniciarSesion():
    channel = grpc.insecure_channel('localhost:50051')
    #channel = grpc.insecure_channel('192.168.4.246:50051')
    stub = Registry_pb2_grpc.loginStub(channel)
    response = stub.Login(Registry_pb2.loginRequest(username="alfonsox1",password="12345"))
    print("Client received: " + response.response)
    return response.response

    
def modificarUsuario():
    channel = grpc.insecure_channel('localhost:50051')
    #channel = grpc.insecure_channel('192.168.4.246:50051')
    stub = Registry_pb2_grpc.modifyUserStub(channel)
    response = stub.Modify(Registry_pb2.changeUserInfo
        (username="alfonsox1",password="12346",newUsername="alfonsox1",newPassword="12345"))
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




@atexit.register
#HACER QUE DESAPAREZCA O SE DESCONECTE DE ENGINE AL SALIR
def goodbye():
    print('You are now leaving the Python sector.')

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.

    if(len(sys.argv) != 5):
        print("Para ejecutar utiliza: FWQ_Sensor.py |IP GRPC SERVER| |PUERTO| |IP BROCKER SERVER| |PUERTO|")
    else:
        serverGrpc = sys.argv[1]
        puertoGrpc = sys.argv[2]
        serverKafka = sys.argv[3]
        puertoKafa=sys.argv[4]

        fila=0
        columna=0

        #FALTA RECIBIR POR ARGUMENTO LOS IP Y PUETOS
        #Elige al azar una de las atracciones con menos de 60 minutos de espera y va hacia ella
        #Si en el camino cambia a tener 60 minuos o mas elige otra.
        #Cada segundo dara un paso en una de la 8 direcciones
        matriz = np.full((20,20), '---')
        matriz[2][2]='a1'
        matriz[4][9]='a2'
        matriz[13][18]='a3'
        matriz[5][1]='a4'
        matriz[8][8]='a5'
        print(matriz)

        opcion=0
        while(opcion!=1 or opcion!= 2 or opcion!=3):
            print("Eliga una opcion: \n 1) Registrarse; \n 2) Iniciar sesion; \n 3) Modificar usuario;\n 4) Salir;")
            opcion = input()
            if opcion == "1":
                registarse()
            if opcion == "2":
                print(iniciarSesion())
            if opcion == "3":
                modificarUsuario()
            if opcion =="4":
                break
        
        print("Hasta pronto!")

if __name__ == "__main__":
    logging.basicConfig()
    run()
