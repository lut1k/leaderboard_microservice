import random
import pika
import json
import time


AMQP_USER = 'admin'
AMQP_PASSWORD = 'admin'
AMQP_HOST = 'localhost'
AMQP_PORT = 5672
AMQP_VIRTUALHOST = '/'


def main():
    credentials = pika.PlainCredentials(AMQP_USER, AMQP_PASSWORD)
    parameters = pika.ConnectionParameters(AMQP_HOST, AMQP_PORT, AMQP_VIRTUALHOST, credentials)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.exchange_declare(exchange='leaderboard_exchange', exchange_type='direct')

    channel.queue_declare(queue='leaderboard_queue', durable=True)

    channel.queue_bind(queue='leaderboard_queue', exchange='leaderboard_exchange')

    index = 100
    while index < 110:
        message = {
            'user_id': index,
            'rating': round(random.uniform(1, 10), 1),
            'datetime': int(time.time()),
        }

        channel.basic_publish(
            exchange='leaderboard_exchange',
            routing_key='leaderboard_queue',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ),
        )

        print(" [x] Sent {}".format(message))

        index += 1

    connection.close()


if __name__ == '__main__':
    main()
