import pika
import json
import datetime
import sys
import traceback
from leaderboard.models import LeaderBoard
from tima_microservice.settings import AMQP_SETTINGS


class RecevieMessages:
    # TODO нужно ли описывать конструктор???

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

        result = channel.queue_declare(queue='', durable=True, exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(queue=queue_name,
                           exchange=AMQP_SETTINGS["AMQP_EXCHANGE_NAME"],
                           routing_key=AMQP_SETTINGS["AMQP_ROUTING_KEY"],
                           )

        print(" [*] Waiting for messages. To exit press CTRL + C.")

        channel.basic_consume(
            queue=queue_name,
            on_message_callback=self.callback,
        )

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        except Exception:
            channel.stop_consuming()
            traceback.print_exc(file=sys.stdout)
