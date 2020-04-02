import pika
import json
import datetime
import sys
import traceback
from django.conf import settings
from leaderboard.models import LeaderBoard


AMQP_SETTINGS = {
    'AMQP_USER': settings.AMQP_SETTINGS['AMQP_USER'],
    "AMQP_PASSWORD": settings.AMQP_SETTINGS['AMQP_PASSWORD'],
    "AMQP_HOST": settings.AMQP_SETTINGS['AMQP_HOST'],
    "AMQP_PORT": settings.AMQP_SETTINGS['AMQP_PORT'],
    "AMQP_VIRTUALHOST": settings.AMQP_SETTINGS['AMQP_VIRTUALHOST'],
    "AMQP_EXCHANGE_NAME": settings.AMQP_SETTINGS['AMQP_EXCHANGE_NAME'],
    "AMQP_QUEUE_NAME": settings.AMQP_SETTINGS['AMQP_QUEUE_NAME'],
    "AMQP_ROUTING_KEY": settings.AMQP_SETTINGS['AMQP_ROUTING_KEY'],
}


class RecevieMessages:
    @staticmethod
    def callback(channel, method, properties, body):
        message = json.loads(body)
        player_attributes = {
            'user_id': message['user_id'],
            'rating': message['rating'],
            'date_time': datetime.datetime.fromtimestamp(message['datetime']),
            'position': message['position']
        }

        player = LeaderBoard(**player_attributes)
        player.save()

        channel.basic_ack(delivery_tag=method.delivery_tag)

    @staticmethod
    def _get_connection():
        credentials = pika.PlainCredentials(AMQP_SETTINGS['AMQP_USER'], AMQP_SETTINGS['AMQP_PASSWORD'])

        parameters = pika.ConnectionParameters(AMQP_SETTINGS['AMQP_HOST'],
                                               AMQP_SETTINGS['AMQP_PORT'],
                                               AMQP_SETTINGS['AMQP_VIRTUALHOST'],
                                               credentials,
                                               )

        return pika.BlockingConnection(parameters)

    def run(self):
        connection = self._get_connection()
        channel = connection.channel()

        channel.queue_declare(queue=AMQP_SETTINGS["AMQP_QUEUE_NAME"], durable=True)

        print(" [*] Waiting for messages. To exit press CTRL + C.")

        channel.basic_consume(
            queue=AMQP_SETTINGS["AMQP_QUEUE_NAME"],
            on_message_callback=self.callback,
        )

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        except Exception:
            channel.stop_consuming()
            traceback.print_exc(file=sys.stdout)
