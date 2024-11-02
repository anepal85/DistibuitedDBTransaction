
# common/publisher.py
import pika
import json

def publish_message(routing_key, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='events', exchange_type='topic')
    channel.basic_publish(
        exchange='events',
        routing_key=routing_key,
        body=json.dumps(message)
    )
    connection.close()
