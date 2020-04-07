import time
from django.core.management import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Start the process of refreshing materialized view 'leaderboard_view'."

    def handle(self, *args, **options):
        self.refresh_materialized_view()

    def refresh_materialized_view(self):
        self.stdout.write("Start the process of refreshing materialized view 'leaderboard_view'.")
        while True:
            with connection.cursor() as cursor:
                cursor.execute("REFRESH MATERIALIZED VIEW leaderboard_view")
            self.stdout.write("REFRESH MATERIALIZED VIEW leaderboard_view.")
            time.sleep(30)
