from kafka import KafkaProducer
from kafka import KafkaConsumer

#mapa en bloc de notas (SI)
producer = KafkaProducer(bootstrap_servers='192.168.3.77:9092')
producer.send('h', b'hola!2')
producer.flush()
producer.close()

pasos = KafkaConsumer('respuesta',bootstrap_servers='192.168.3.77:9092')#,auto_offset_reset='latest')
#print(value)
for message in pasos:
    print (message)
    