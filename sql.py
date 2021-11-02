import sqlite3

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

#c.execute("""INSERT INTO usuarios (val) VALUES ()"""),

str=""". . . . . . . . . a1 . . . . . . . a14 . .
\n. . . . . . . . . . . . . . . . . . . .
\n. . . . . . a6 . . . . . . . . . . . . .
\n. . . . a7 . . . . . . . . . . . . . . .
\n. . . . . . a2 . . . . . . . . . . . . .
\n. . . . . . . . . . . . . . . . . . . .
\n. . . . . . . . . . . . . . . . . a9 . .
\n. . . . . . . . . . . . . . . . . . . .
\n. . . a8 . . . . . . . . . . . . . . . a5
\n. . . . . . . . . . . . . . . . . . . .
\n. . . . . . . . . . a15 . . . . . . . . .
\n. . . . . . . . . . . . . . . . . . . .
\n. . . . . . . . . . . . . . . . . . . .
\n. . . . . . . . . . . . . a10 . . . . . .
\n. . . . . . . . . . . . . . . . . . . .
\n. . . . . a3 . . . . . . . . . . . . . .
\n. . . . . . a12 . . . . . . . . . . . . .
\n. . . . . . . . . . . . . . . . . . . .
\n. . . . . . . a4 . . . . . . . . . . . .
\n. . . . . . . . . . . . . . . a13 . . . .\n"""
print(str)
conn.commit()