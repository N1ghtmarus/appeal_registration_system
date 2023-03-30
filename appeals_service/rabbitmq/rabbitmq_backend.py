import os
import sys

import pika

from appeal_to_fastapi import post_appeal_to_fastapi


def rabbitmq_receiver():
    """
    Устанавливает соединение с RabbitMQ и ожидает сообщения в очереди tornado_task.
    После получения сообщения вызывает функцию post_appeal_to_fastapi,
    передавая тело сообщения в качестве аргумента.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='tornado_task')

    def callback(ch, method, properties, body):
        print(" [x] Appeal recieved %r" % body.decode())
        post_appeal_to_fastapi(body)

    channel.basic_consume(queue='tornado_task', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for appeals. Press CTRL+C to exit.')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        rabbitmq_receiver()
    except KeyboardInterrupt:
        print('Program was interrupted during the execution')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
