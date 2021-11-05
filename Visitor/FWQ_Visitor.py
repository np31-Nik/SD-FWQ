from __future__ import print_function
from kafka import KafkaConsumer
from kafka import KafkaProducer
import numpy as np
from numpy import random
import logging
import grpc
import atexit
import sys

sys.path.append('C:/Users/serg2/source/repos/SD-FWQ/Registry')
import Registry_pb2
import Registry_pb2_grpc

#Revisar
def enviarPaso(id,fila,columna,server,puerto):
    producer = KafkaProducer(bootstrap_servers=['%s:%s' %(server,puerto)])
    mensaje = '%s:%s:%s' %(id,str(fila),str(columna))
    producer.send('sensorPersonas', bytes(mensaje,'UTF-8'))
    producer.flush()
    #print(msg) ????


#falta hacer
def recibirMapa():
    return True



#Cuenta numero de atracciones y luego elige una random
def buscarAtraccion(mapa): 
    contador =0 #Contador de atracciones
    for row in mapa:
        for col in mapa:
            if mapa[row][col]!='---':
                contador=contador+1

    atraccion=random.randint(contador) #comprobar si funciona
    contador =0
    for row in mapa:
        for col in mapa:
            if mapa[row][col]!='---':
                contador=contador+1
                if contador==atraccion: 
                    return row,col


def moverse(id,server,port):
    fila=0
    columna=0
    filaAtraccion=-1 
    colAtraccion=-1
    while(True):
        map=recibirMapa()
        while filaAtraccion==-1:
            filaAtraccion,colAtraccion=buscarAtraccion(map)
        fila,columna=calcularPaso(fila,columna,filaAtraccion,colAtraccion)
        enviarPaso(id,fila,columna,server,port)


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

    return fila,columna




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


def iniciarSesion(UserID):
    channel = grpc.insecure_channel('localhost:50051')
    #channel = grpc.insecure_channel('192.168.4.246:50051')
    stub = Registry_pb2_grpc.loginStub(channel)
    username,password=AskNamePassword()
    response = stub.Login(Registry_pb2.loginRequest(username=username,password=password))
    #response = stub.Login(Registry_pb2.loginRequest(username="alfonsox1",password="12345"))
    print("Client received: " + response.response)
    if response.response!="El nombre de usuario o la contraseña no son correctos":
        UserID=response.response
        return True
    else:
        print(response.response)
        return False



    
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


        UserID="-1"

        matriz = np.full((20,20), '---')
        matriz[2][2]='a1'
        matriz[4][9]='a2'
        matriz[13][18]='a3'
        matriz[5][1]='a4'
        matriz[8][8]='a5'
        print(matriz)

        opcion=0
        while True:
            print("Eliga una opcion: \n 1) Registrarse; \n 2) Iniciar sesion y entrar al parque; \n 3) Modificar usuario;\n 4) Salir;")
            opcion = input()
            if opcion == "1":
                registarse()
            if opcion == "2":

                #****Luego quitar****
                serverKafka=1
                puertoKafka=2

                if iniciarSesion(UserID,serverKafka,puertoKafka):
                    moverse(UserID,serverKafka,puertoKafka)
                
            if opcion == "3":
                modificarUsuario()
            if opcion =="4":
                break
        
        print("Hasta pronto!")

if __name__ == "__main__":
    logging.basicConfig()
    run()
