from kafka import KafkaConsumer
import sys

bootstrap_servers = ['localhost:9092']
topicName = 'secure-suite-maxwell'

consumer = KafkaConsumer (topicName, api_version=(0, 10, 1), bootstrap_servers=bootstrap_servers)

print("Listening for stream events...\n")
try:
    for message in consumer:
        print ("%s:%d:%d: key=%s value=%s\n" % (message.topic, message.partition,message.offset, message.key,message.value))
except KeyboardInterrupt:
    sys.exit()
