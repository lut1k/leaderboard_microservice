from django.core.management import BaseCommand
from leaderboard.receive_messages import RecevieMessages


class Command(BaseCommand):
    help = "Starts the AMQP-server with parameters: "

    def handle(self, *args, **options):
        consumer = RecevieMessages()
        consumer.run()
