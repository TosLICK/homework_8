import pika
import json
import pickle

# from datetime import datetime
from random import randint
from faker import Faker

import connect
from models import Contact


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='task_mock', exchange_type='direct')
# channel.queue_declare(queue='email_queue', durable=True)
# channel.queue_declare(queue='sms_queue', durable=True)
channel.queue_declare(queue='task_queue', durable=True)
channel.queue_bind(exchange='task_mock', queue='task_queue')


def main():
    for i in range(4):
    #         message = {
    #         "id": i + 1,
    #         "payload": f"Task #{i + 1}",
    #         "date": datetime.now().isoformat()
    #     }
        contact = Contact(
            fullname=Faker().name(),
            email=Faker().email(),
            phone=Faker().phone_number(),
            prefered_channel=Faker().random_element(['email', 'sms']),
            received_message=False
        ).save()

        # message = {
            # "id": contact.id
            # "fullname": contact.fullname,
            # "email": contact.email,
            # "phone": contact.phone,
            # "received_message": contact.received_message,
            # "date": datetime.now().isoformat()
        # }
        message = str(contact.id)

        if contact.prefered_channel == 'email':
            channel.basic_publish(
                exchange='task_mock',
                routing_key='task_queue',
                # routing_key='email_queue',
                body=message.encode(),
                # body=json.dumps(message).encode(),
                # body=pickle.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ))
        elif contact.prefered_channel == 'sms': 
            channel.basic_publish(
                exchange='task_mock',
                routing_key='task_queue',
                # routing_key='sms_queue',
                body=message.encode(),
                # body=json.dumps(message).encode(),
                # body=pickle.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ))
        # channel.basic_publish(
        #     exchange='task_mock',
        #     routing_key='task_queue',
        #     body=message.encode(),
        #     # body=json.dumps(message).encode(),
        #     # body=pickle.dumps(message),
        #     properties=pika.BasicProperties(
        #         delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        #     ))
        print(" [x] Sent %r" % message)
    connection.close()
    
    
if __name__ == '__main__':
    main()
