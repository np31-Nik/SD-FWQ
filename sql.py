import sqlite3

conn = sqlite3.connect('db.db')

c=conn.cursor()

#c.execute("""CREATE TABLE usuarios(
 #   id text,
  #  name text,
   # password text
    #)""")
c.execute("""INSERT INTO usuarios VALUES ('u1', 'Pedro Lopez', '12345');""")
#c.execute("""SELECT * from usuarios""")
conn.commit()