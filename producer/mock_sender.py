import random
import sys
import pika
import json
import time


AMQP_SETTINGS = {
    'AMQP_USER': 'admin',
    "AMQP_PASSWORD": 'admin',
    "AMQP_HOST": 'localhost',
    "AMQP_PORT": 5672,
    "AMQP_VIRTUALHOST": '/',
    "AMQP_EXCHANGE_NAME": 'leaderboard_exchange',
    "AMQP_QUEUE_NAME": 'leaderboard_queue',
    "AMQP_ROUTING_KEY": 'leaderboard_key',
}


class MockSender:
    @staticmethod
    def _get_connection():
        credentials = pika.PlainCredentials(AMQP_SETTINGS["AMQP_USER"],
                                            AMQP_SETTINGS["AMQP_PASSWORD"])

        parameters = pika.ConnectionParameters(AMQP_SETTINGS["AMQP_HOST"],
                                               AMQP_SETTINGS["AMQP_PORT"],
                                               AMQP_SETTINGS["AMQP_VIRTUALHOST"],
                                               credentials,
                                               )
        return pika.BlockingConnection(parameters)

    def start_sending(self):
        connection = self._get_connection()

        channel = connection.channel()

        channel.exchange_declare(exchange=AMQP_SETTINGS["AMQP_EXCHANGE_NAME"], exchange_type='direct')
        channel.queue_declare(queue=AMQP_SETTINGS["AMQP_QUEUE_NAME"], durable=True)
        channel.queue_bind(queue=AMQP_SETTINGS["AMQP_QUEUE_NAME"],
                           exchange=AMQP_SETTINGS["AMQP_EXCHANGE_NAME"],
                           routing_key=AMQP_SETTINGS["AMQP_ROUTING_KEY"],
                           )

        try:
            while True:
                random_user_id = random.randint(1, 3000000)
                message = {
                    'user_id': random_user_id,
                    'rating': round(random.uniform(1, 100), 1),
                    'datetime': int(time.time()),
                }
                channel.basic_publish(
                    exchange=AMQP_SETTINGS["AMQP_EXCHANGE_NAME"],
                    routing_key=AMQP_SETTINGS["AMQP_ROUTING_KEY"],
                    body=json.dumps(message),
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # make message persistent
                    ),
                )
                sys.stdout.write(" [x] Sent {}\n".format(message))
                time.sleep(0.02)
        except KeyboardInterrupt:
            connection.close()


if __name__ == '__main__':
    producer = MockSender()
    producer.start_sending()
