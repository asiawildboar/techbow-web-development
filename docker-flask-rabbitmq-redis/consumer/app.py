#!/usr/bin/env python
import pika
import redis


def callback(ch, method, properties, body):
    print(" [x] Received temperature %r" % body)
    cur_temp = int(body)
    redis_client = redis.Redis(host='redis-host', port=6379, db=0)
    if redis_client.get("total") == None:
        redis_client.set("total", cur_temp)
        redis_client.set("num", 1)
    else:
        redis_client.set("total", int(redis_client.get("total")) + cur_temp)
        redis_client.set("num", int(redis_client.get("num")) + 1)


connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-host'))
channel = connection.channel()

channel.queue_declare(queue='demo-temperature')

channel.basic_consume(queue='demo-temperature', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()  
