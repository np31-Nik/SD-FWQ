import sqlite3

conn = sqlite3.connect('db.db')

c=conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS atracciones(
    id text PRIMARY KEY,
    visitantesCiclo int NOT NULL,
    tiempoCiclo int NOT NULL
    )""")
    
c.execute("""CREATE TABLE IF NOT EXISTS Mapa(
    id text PRIMARY KEY,
    x int NOT NULL,
    y int NOT NULL,
    valor text,
    FOREIGN KEY (valor) REFERENCES atracciones (id)
    )""")


c.execute("""INSERT INTO atracciones VALUES ('a1', 'Pedro Lopez', '12345');""")
#c.execute("""SELECT * from usuarios""")
conn.commit()