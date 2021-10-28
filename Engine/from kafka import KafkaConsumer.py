from kafka import KafkaConsumer
from kafka import KafkaProducer

#mapa en bloc de notas (SI)
producer = KafkaProducer(bootstrap_servers='192.168.3.246:9092')
producer.send('sample', b'hola!')

pasos = KafkaConsumer('respuesta',bootstrap_servers='192.168.3.246:9092',auto_offset_reset='latest')
#print(value)
for message in pasos:
    print (message)
    break
    