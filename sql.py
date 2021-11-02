import sqlite3
import random

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
id_mapa = 1

for i in range(1,17):

    visit = random.randint(1,5)
    tiempo = random.randint(1,10)
    #print("x: "+str(x[i])+" y: "+str(y[i]))
    #print(str(i))

    c.execute("""INSERT INTO Mapa(id,x,y,valor) VALUES (%s,%s,%s,%s)""" %(id_mapa,str(x[i]),str(y[i]),"a"+str(i)))
    c.execute("""INSERT INTO Matracciones(id,visitantesCiclo,tiempoCiclo) VALUES (%s,%s,%s)""" %("a"+str(i),str(visit),str(tiempo)))




conn.commit()