from kafka import KafkaConsumer
from kafka import KafkaProducer

#mapa en bloc de notas (SI)

pasos = KafkaConsumer('sample')
for message in pasos:
    print (message)
    producer = KafkaProducer(bootstrap_servers='192.168.3.246:9092')
    producer.send('respuesta', b'hola!')
    print("Hola")