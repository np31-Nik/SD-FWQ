from concurrent import futures

import logging
import grpc
import Registry_pb2
import Registry_pb2_grpc
import sqlite3

conn = sqlite3.connect('db.db')
c=conn.cursor()



def usuarioEnBDLogin(name, password):
	#conectranos a la BD
	conn = sqlite3.connect('db.db')
	c=conn.cursor()
	c.execute("""SELECT username, password from usuarios""")
	usuario=c.fetchall()
	login=False
	for i in usuario:
		if i[0] == name and i[1]==password:
			login=True 
	if login:#consultamos BD con name
		return "Bienvenido"
	else: #la contraseña no es correcta
		return "El usuario o la contraseña no son correctos"

def Registro(name, password):
<<<<<<< HEAD
	# conn = sqlite3.connect('db.db')
	# c=conn.cursor()
	# c.execute("""SELECT username from usuarios""")
	# usuario=c.fetchall()
	# yaExiste=False
	# for i in usuario:
	# 	if i[0] == name:
	# 		yaExiste=True 
	# if yaExiste:#consultamos BD con name
	# 	return "El nombre de usaurio ya esta registrado"
	# else:
	# 	Registry.siguienteUsuario=Registry.siguienteUsuario + 1 
	# 	c.execute("""INSERT INTO usuarios (id,username,password) VALUES (?,?,?)""",
	# 	(Registry.siguienteUsuario,name, password))
	return "hola"
=======
	conn = sqlite3.connect('db.db')
	c=conn.cursor()
	c.execute("""SELECT username from usuarios""")
	usuario=c.fetchall()
	yaExiste=False
	for i in usuario:
		if i[0] == name:
			yaExiste=True 
	if yaExiste:#consultamos BD con name
		return "El nombre de usaurio ya esta registrado"
	else:
		Registry.siguienteUsuario=Registry.siguienteUsuario + 1 
		c.execute("""INSERT INTO usuarios (id,username,password) VALUES (?,?,?)""",
		(Registry.siguienteUsuario,name, password))
>>>>>>> a6ad709b4e4e5385394f6259b762430856ff2906


class Registry(Registry_pb2_grpc.RegistryServiceServicer):
	siguienteUsuario=2
	def Registry(self,request,context):
		Registro(request.name, request.password)
		return Registry_pb2.RegistryResponse(response="Usuario anyadido a la base de datos(hola)")


def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	Registry_pb2_grpc.add_RegistryServiceServicer_to_server(Registry(), server)
	server.add_insecure_port('[::]:50051')
	server.start()
	server.wait_for_termination()


if __name__ == '__main__':
	logging.basicConfig()
	serve()
