import pika

from random import randint
from faker import Faker

import connect
from models import Contact


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='task_mock', exchange_type='direct')
channel.queue_declare(queue='email_queue', durable=True)
channel.queue_declare(queue='sms_queue', durable=True)
channel.queue_bind(exchange='task_mock', queue='email_queue', routing_key='email')
channel.queue_bind(exchange='task_mock', queue='sms_queue', routing_key='sms')


def main():
    contact_num = randint(4, 6)
    for i in range(contact_num):
        contact = Contact(
            fullname=Faker().name(),
            email=Faker().email(),
            phone=Faker().phone_number(),
            prefered_channel=Faker().random_element(['email', 'sms']),
            sent_message=False
        ).save()

        message = str(contact.id)

        if contact.prefered_channel == 'email':
            channel.basic_publish(
                exchange='task_mock',
                routing_key='email',
                body=message.encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ))
        elif contact.prefered_channel == 'sms': 
            channel.basic_publish(
                exchange='task_mock',
                routing_key='sms',
                body=message.encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ))

        print(" [x] Sent %r" % message)
    connection.close()
    
    
if __name__ == '__main__':
    main()
