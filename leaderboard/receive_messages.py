import pika
import json
import datetime
import sys
from django.conf import settings
from django.db import transaction

from leaderboard.models import LeaderBoard


class ReceiveMessages:
    @staticmethod
    def callback(channel, method, properties, body):
        message = json.loads(body)
        player_from_message = LeaderBoard(user_id=message['user_id'],
                                          rating=message['rating'],
                                          date_time=datetime.datetime.fromtimestamp(message['datetime']),
                                          )

        with transaction.atomic():
            player_from_db = LeaderBoard.objects.select_for_update().filter(user_id=message['user_id']).first()
            if player_from_db:
                player_from_db.save(update_fields=('rating', 'date_time'))
                sys.stdout.write("Updated data for player with user_id - {}.\n".format(player_from_db.user_id))
                return channel.basic_ack(delivery_tag=method.delivery_tag)

        player_from_message.save()
        sys.stdout.write("Created user with user_id <{}>.\n".format(player_from_message.user_id))
        channel.basic_ack(delivery_tag=method.delivery_tag)

    @staticmethod
    def _get_connection():
        credentials = pika.PlainCredentials(settings.AMQP_SETTINGS['AMQP_USER'],
                                            settings.AMQP_SETTINGS['AMQP_PASSWORD'],
                                            )

        parameters = pika.ConnectionParameters(settings.AMQP_SETTINGS['AMQP_HOST'],
                                               settings.AMQP_SETTINGS['AMQP_PORT'],
                                               settings.AMQP_SETTINGS['AMQP_VIRTUALHOST'],
                                               credentials,
                                               )

        return pika.BlockingConnection(parameters)

    def run(self):
        connection = self._get_connection()
        channel = connection.channel()

        channel.queue_declare(queue=settings.AMQP_SETTINGS["AMQP_QUEUE_NAME"], durable=True)

        sys.stdout.write(" [*] Waiting for messages. To exit press CTRL + C.\n")

        channel.basic_consume(
            queue=settings.AMQP_SETTINGS["AMQP_QUEUE_NAME"],
            on_message_callback=self.callback,
        )

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
