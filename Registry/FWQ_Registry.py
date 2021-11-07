from concurrent import futures

import logging
import grpc
import Registry_pb2
import Registry_pb2_grpc
import sqlite3
import sys



def IniciarSesion(username, password):
	#conectranos a la BD
	conn = sqlite3.connect('../db.db')
	c=conn.cursor()
	try:
		c.execute("""SELECT username, password, id from usuarios""")
		usuario=c.fetchall()
		login=False
		id="-1"
		for i in usuario:
			if i[0] == username and i[1]==password:
				login=True
				id= i[2]
				break
		if login:#consultamos BD con name
			return id
		else: #la contraseña no es correcta
			return id
	except:
		print ("Ha ocurrido un errror al conectarse a la base de datos(Iniciar Sesion)")
		return False
		


def Registro(name, password):
	conn = sqlite3.connect('../db.db')
	c=conn.cursor()
	c.execute("""SELECT username from usuarios""")
	usuario=c.fetchall()
	yaExiste=False
	for i in usuario:
		if i[0] == name:
			yaExiste=True 
	if yaExiste:#consultamos BD con name
		conn.close()
		return "El nombre de usaurio ya esta registrado"
	else:
		try:
			Registry.siguienteUsuario=Registry.siguienteUsuario + 1 
			c.execute("""Insert into usuarios (id,username,password) values(?,?,?)""",
			("u"+str(Registry.siguienteUsuario),name,password))
			resultado="Usuario registrado"
			conn.commit()
			conn.close()
		except:
			resultado ="Error al insertar"
			conn.close()
		return resultado
	

def ModificarUsuario(username, newUsername, newPassword):
	conn = sqlite3.connect('../db.db')
	c=conn.cursor()
	try:
		c.execute("""Update usuarios set username=?, password = ? where username=?""",
		(newUsername,newPassword,username))
		conn.commit()
		conn.close()
		return True
	except:
		conn.close()
		return False




class Registry(Registry_pb2_grpc.RegistryServiceServicer):
	siguienteUsuario=2
	def Registry(self,request,context):
		resul=Registro(request.name, request.password)
		return Registry_pb2.RegistryResponse(response=resul)

class Login(Registry_pb2_grpc.loginServicer):
	def Login(self,request,context):
		id=IniciarSesion(request.username, request.password)
		if id!="-1":
			resul=id
		else:
			resul="El nombre de usuario o la contraseña no son correctos"
		return Registry_pb2.RegistryResponse(response=resul)

class Modify(Registry_pb2_grpc.modifyUserServicer):
	def Modify(self,request,context):
		if(IniciarSesion(request.username,request.password)):
			ModificarUsuario(request.username, request.newUsername,request.newPassword)
			resul="Informacion de usuario modificada"
		else:
			resul="El nombre de usuario o la contraseña no son correctos"
		return Registry_pb2.RegistryResponse(response=resul)

def serve():

	if(len(sys.argv) != 5):
		print("Para ejecutar utiliza: FWQ_Sensor.py |PUERTO GRPC|")
	else:
		puertoGrpc = sys.argv[1]
	
		server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
		Registry_pb2_grpc.add_RegistryServiceServicer_to_server(Registry(), server)
		Registry_pb2_grpc.add_loginServicer_to_server(Login(), server)
		Registry_pb2_grpc.add_modifyUserServicer_to_server(Modify(),server)
		server.add_insecure_port('[::]:%s'%(puertoGrpc))
		server.start()
		server.wait_for_termination()


if __name__ == '__main__':
	logging.basicConfig()
	serve()
