from kafka import KafkaConsumer
from kafka import KafkaProducer





print("hola1")
pasos = KafkaConsumer('sample',bootstrap_servers='localhost:9092')#,auto_offset_reset='latest')
#print(value)
for message in pasos:
    print (message)
    break
    