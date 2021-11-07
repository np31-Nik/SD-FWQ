import sqlite3
import random
import numpy as np

#from FWQ_Registry import usuarioEnBDLogin

conn = sqlite3.connect('db.db')

c=conn.cursor()

# c.execute("""CREATE TABLE IF NOT EXISTS atracciones(
#     id text PRIMARY KEY,
#     visitantesCiclo int NOT NULL,
#     tiempoCiclo int NOT NULL
#     )""")
    
# c.execute("""CREATE TABLE IF NOT EXISTS Mapa(
#     id text,
#     x int NOT NULL,
#     y int NOT NULL,
#     valor text,
#     PRIMARY KEY (id,x,y),
#     FOREIGN KEY (valor) REFERENCES atracciones (id)
#     )""")
#c.execute("Drop Table mapa")
# print(c.execute("""SELECT * from usuarios"""))
# usuario=c.fetchall()
# print(usuario[0][1])


# x = random.sample(range(20),16)
# y = random.sample(range(20),16)
# id_mapa = "m1"

# for i in range(1,17):

#     visit = random.randint(1,5)
#     tiempo = random.randint(1,10)
#     #print("x: "+str(x[i])+" y: "+str(y[i]))
#     #print(str(i))
#     atr = "a"+str(i)
#     #c.execute("""INSERT INTO atracciones(id,visitantesCiclo,tiempoCiclo) VALUES (?,?,?)""" ,(atr,str(visit),str(tiempo)))
#     c.execute("""INSERT INTO Mapa(id,x,y,valor) VALUES (?,?,?,?)""",(id_mapa,x[i-1],y[i-1],atr))
#     # c.execute("""INSERT INTO atracciones(id,visitantesCiclo,tiempoCiclo) VALUES (%s,%s,%s)""" %(atr,str(visit),str(tiempo)))
#     # c.execute("""INSERT INTO Mapa(id,x,y,valor) VALUES (%s,%s,%s,%s)""" %(id_mapa,str(x[i]),str(y[i]),atr))


c.execute("Delete from usuarios where id='u3'")

#c.execute("Select valor,x,y from mapa")
# lista=[[]]
# cont=0
# result=c.fetchall()
# lista=result
# print(result)
# # for val in result:
# #     lista[cont][0]=val[0]
# #     lista[cont][1]=val[1]
# #     lista[cont][2]=val[2]
# #     cont=cont+1
# print((lista[0][0]))

# ej = np.full((3,3),1)
# for i in range(len(ej)):
#     #for j in range(len(ej[i])):
#     print(ej[i])

conn.commit()
conn.close()