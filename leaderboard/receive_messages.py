import pika
import json
import datetime
import sys
import traceback


AMQP_USER = 'admin'
AMQP_PASSWORD = 'admin'
AMQP_HOST = 'localhost'
AMQP_PORT = 5672
AMQP_VIRTUALHOST = '/'


def callback(channel, method, properties, body):
    print(" [x] Received {}".format(body))

    message = json.loads(body)

    print('user_id : {}, rating : {}, datetime : {}'.format(
        message['user_id'],
        message['rating'],
        datetime.datetime.fromtimestamp(message['datetime']),
    ))

    print('[x] Done.')

    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    credentials = pika.PlainCredentials(AMQP_USER, AMQP_PASSWORD)
    parameters = pika.ConnectionParameters(AMQP_HOST, AMQP_PORT, AMQP_VIRTUALHOST, credentials)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.queue_declare(queue='leaderboard_queue', durable=True)

    print(" [*] Waiting for messages. To exit press CTRL + C.")

    channel.basic_consume(
        queue='leaderboard_queue',
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
