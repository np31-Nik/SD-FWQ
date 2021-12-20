import random
def leer():
    archivo = "ciudades.txt"
    f= open(archivo,'r')

    r = f.read()
    r = r.split(',')
    ciudades=[]
    i = 0
    while i < 4:
        rand = random.randint(0,len(r)-1)
        if r[rand] not in ciudades:
            ciudades.append(r[rand])
            i += 1
    f.close()
    return r

leer()