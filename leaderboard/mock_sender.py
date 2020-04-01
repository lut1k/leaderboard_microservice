import random
import pika
import json
import time
from tima_microservice.settings import AMQP_SETTINGS


class MockSender:
    @staticmethod
    def _get_connection():
        credentials = pika.PlainCredentials(AMQP_SETTINGS["AMQP_USER"], AMQP_SETTINGS["AMQP_PASSWORD"])

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

        index = 1
        while index:
            message = {
                'user_id': index,
                'rating': round(random.uniform(1, 10), 1),
                'datetime': int(time.time()),
                'position': index,  # TODO убарть позицию из сообщения после изучения memcached.
            }
            channel.basic_publish(
                exchange=AMQP_SETTINGS["AMQP_EXCHANGE_NAME"],
                routing_key=AMQP_SETTINGS["AMQP_ROUTING_KEY"],
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ),
            )

            print(" [x] Sent {}".format(message))
            index += 1
            time.sleep(0.02)

        connection.close()


if __name__ == '__main__':
    producer = MockSender()
    producer.start_sending()
