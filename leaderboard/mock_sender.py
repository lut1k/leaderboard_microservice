import random
import pika
import json
import time


AMQP_USER = 'admin'
AMQP_PASSWORD = 'admin'
AMQP_HOST = 'localhost'
AMQP_PORT = 5672
AMQP_VIRTUALHOST = '/'
AMQP_EXCHANGE_NAME = 'leaderboard_exchange'
AMQP_ROUTING_KEY = 'leaderboard_key'


def main():
    credentials = pika.PlainCredentials(AMQP_USER, AMQP_PASSWORD)
    parameters = pika.ConnectionParameters(AMQP_HOST, AMQP_PORT, AMQP_VIRTUALHOST, credentials)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.exchange_declare(exchange=AMQP_EXCHANGE_NAME, exchange_type='direct')

    index = 100
    while index < 150:
        message = {
            'user_id': index,
            'rating': round(random.uniform(1, 10), 1),
            'datetime': int(time.time()),
            'position': index,  # TODO убарть позицию из сообщения после изучения memcached.
        }

        channel.basic_publish(
            exchange=AMQP_EXCHANGE_NAME,
            routing_key=AMQP_ROUTING_KEY,
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
