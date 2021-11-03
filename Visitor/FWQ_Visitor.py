from __future__ import print_function

import logging

import grpc

import atexit

import sys
sys.path.append('C:/Users/serge/source/repos/SD-FWQ/Registry')
import Registry_pb2
import Registry_pb2_grpc


def regisrtarse():
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
        (username="alfonsox1",password="12345",newUsername="alfonsox1",newPassword="12346"))
    print("Client received: " + response.response)
    return response.response


@atexit.register
def goodbye():
    print('You are now leaving the Python sector.')

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.

    #FALTA RECIBIR POR ARGUMENTO LOS IP Y PUETOS

    opcion=0
    while(opcion!=1 or opcion!= 2 or opcion!=3):
        print("Eliga una opcion: \n 1) Registrarse; \n 2) Iniciar sesion; \n 3) Modificar usuario;\n 4) Salir;")
        opcion = input()
        if opcion == "1":
            regisrtarse()
        if opcion == "2":
            print(iniciarSesion())
        if opcion == "3":
            modificarUsuario()
        if opcion =="4":
            break
    
    
    print("Hasta pronto!")
    # channel = grpc.insecure_channel('localhost:50051')
    # #channel = grpc.insecure_channel('192.168.4.246:50051')
    # stub = Registry_pb2_grpc.RegistryServiceStub(channel)
    # response = stub.Registry(Registry_pb2.RegistryRequest(ID=1,name="you",password="12345"))
    # print("Client received: " + response.response)

if __name__ == "__main__":
    logging.basicConfig()
    run()
