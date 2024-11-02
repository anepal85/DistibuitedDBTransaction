
# common/subscriber.py
import pika
import json

def subscribe_to(routing_key_pattern):
    def decorator(func):
        def wrapper():
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
            channel.exchange_declare(exchange='events', exchange_type='topic')
            result = channel.queue_declare('', exclusive=True)
            queue_name = result.method.queue
            channel.queue_bind(exchange='events', queue=queue_name, routing_key=routing_key_pattern)
            
            def callback(ch, method, properties, body):
                message = json.loads(body)
                func(message)
            
            channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
            channel.start_consuming()
        return wrapper
    return decorator
