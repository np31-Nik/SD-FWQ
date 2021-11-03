import sqlite3
import random

#from FWQ_Registry import usuarioEnBDLogin

conn = sqlite3.connect('db.db')

c=conn.cursor()

# c.execute("""CREATE TABLE IF NOT EXISTS atracciones(
#     id text PRIMARY KEY,
#     visitantesCiclo int NOT NULL,
#     tiempoCiclo int NOT NULL
#     )""")
    
c.execute("""CREATE TABLE IF NOT EXISTS Mapa(
    id text,
    x int NOT NULL,
    y int NOT NULL,
    valor text,
    PRIMARY KEY (id,x,y),
    FOREIGN KEY (valor) REFERENCES atracciones (id)
    )""")
#c.execute("Drop Table mapa")
# print(c.execute("""SELECT * from usuarios"""))
# usuario=c.fetchall()
# print(usuario[0][1])


x = random.sample(range(20),16)
y = random.sample(range(20),16)
id_mapa = "m1"

for i in range(1,17):

    visit = random.randint(1,5)
    tiempo = random.randint(1,10)
    #print("x: "+str(x[i])+" y: "+str(y[i]))
    #print(str(i))
    atr = "a"+str(i)
    #c.execute("""INSERT INTO atracciones(id,visitantesCiclo,tiempoCiclo) VALUES (?,?,?)""" ,(atr,str(visit),str(tiempo)))
    #c.execute("""INSERT INTO Mapa(id,x,y,valor) VALUES (?,?,?,?)""",(id_mapa,x[i-1],y[i-1],atr))
    # c.execute("""INSERT INTO atracciones(id,visitantesCiclo,tiempoCiclo) VALUES (%s,%s,%s)""" %(atr,str(visit),str(tiempo)))
    # c.execute("""INSERT INTO Mapa(id,x,y,valor) VALUES (%s,%s,%s,%s)""" %(id_mapa,str(x[i]),str(y[i]),atr))

c.execute("Insert into usuarios (id,username,password) values(?,?,?)",("u1","alfonsox1","12345"))
c.execute("Select * from usuarios")
result=c.fetchall()
print((result))

conn.commit()