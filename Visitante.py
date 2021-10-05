import socket
import sys

serverIP = "192.168.56.1"
Port = 5555
Format = 'utf-8'


print ("Iniciando")

#Comprobar argumentos
SERVER = sys.argv[1]
ADDR= (SERVER, Port)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
