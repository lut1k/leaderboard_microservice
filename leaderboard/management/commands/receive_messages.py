from django.core.management import BaseCommand
from leaderboard.receive_messages import RecevieMessages


class Command(BaseCommand):
    def handle(self, *args, **options):
        consumer = RecevieMessages()
        consumer.run()
