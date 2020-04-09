import datetime
from django.test import TestCase
from django.urls import include, path
from leaderboard.management.commands.refresh_leaderboardview import Command
from leaderboard.models import LeaderBoard


class ResponsesTest(TestCase):
    urlpatterns = [
        path('leaderboard/', include('leaderboard.urls')),
    ]

    @classmethod
    def setUpTestData(cls):
        LeaderBoard.objects.create(user_id=10, rating=5.7, date_time=datetime.datetime.now())
        command_for_refresh_view = Command()
        command_for_refresh_view.refresh_materialized_view()

    def test_response_players(self):
        response = self.client.get('/players')
        self.assertEqual(response.data['user_id'], 10)
