import pika
import json
import datetime
import sys
import traceback
from leaderboard.models import LeaderBoard


AMQP_USER = 'admin'
AMQP_PASSWORD = 'admin'
AMQP_HOST = 'localhost'
AMQP_PORT = 5672
AMQP_VIRTUALHOST = '/'
AMQP_EXCHANGE_NAME = 'leaderboard_exchange'
AMQP_ROUTING_KEY = 'leaderboard_key'


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


def main():
    credentials = pika.PlainCredentials(AMQP_USER, AMQP_PASSWORD)
    parameters = pika.ConnectionParameters(AMQP_HOST, AMQP_PORT, AMQP_VIRTUALHOST, credentials)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    result = channel.queue_declare(queue='', durable=True, exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(queue=queue_name,
                       exchange=AMQP_EXCHANGE_NAME,
                       routing_key=AMQP_ROUTING_KEY,
                       )

    print(" [*] Waiting for messages. To exit press CTRL + C.")

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
    )

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    except Exception:
        channel.stop_consuming()
        traceback.print_exc(file=sys.stdout)


if __name__ == '__main__':
    main()
