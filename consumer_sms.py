#!/usr/bin/env python
import json
import pickle
import os
import sys
import time

import pika
import connect
from models import Contact


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='email_queue', durable=True)
    # channel.queue_declare(queue='sms_queue', durable=True)


    def callback(ch, method, properties, body):
        # message = json.loads(body.decode())
        # message = pickle.loads(body)
        pk = body.decode()
        contact = Contact.objects(id=pk, received_message=False).first()
        if contact:
            contact.update(set__received_message=True)
            contact.save()
        print(f" [x] Received {pk}")
        time.sleep(0.5) 
        print(f" [x] Done {method.delivery_tag}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)
    # channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)
    channel.basic_recover(requeue=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)