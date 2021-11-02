import sqlite3

conn = sqlite3.connect('db.db')

c=conn.cursor()


c.execute("""CREATE TABLE IF NOT EXISTS usuarios(
    id text PRIMARY KEY,
    username text NOT NULL,
    password text NOT NULL
    )""")

# c.execute("""CREATE TABLE IF NOT EXISTS atracciones(
#     id text PRIMARY KEY,
#     visitantesCiclo int NOT NULL,
#     tiempoCiclo int NOT NULL
#     )""")
    
# c.execute("""CREATE TABLE IF NOT EXISTS Mapa(
#     id text PRIMARY KEY,
#     x int NOT NULL,
#     y int NOT NULL,
#     valor text,
#     FOREIGN KEY (valor) REFERENCES atracciones (id)
#     )""")

# print(c.execute("""SELECT * from usuarios"""))
# usuario=c.fetchall()
# print(usuario[0][1])


conn.commit()