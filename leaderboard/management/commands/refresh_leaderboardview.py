import time
from django.core.management import BaseCommand
from django.db import connection, transaction


class Command(BaseCommand):
    help = "Start the process of refreshing materialized view 'leaderboard_view'."

    def handle(self, *args, **options):
        self.stdout.write("Start the process of refreshing materialized view 'leaderboard_view'.")
        while True:
            self.refresh_materialized_view()
            time.sleep(30)

    def refresh_materialized_view(self):
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY leaderboard_view")
        self.stdout.write("REFRESH MATERIALIZED VIEW leaderboard_view.")
