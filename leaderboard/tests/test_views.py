import datetime
import json
from django.test import TestCase
from leaderboard.management.commands.refresh_leaderboardview import Command
from leaderboard.models import LeaderBoard


class ResponsesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        LeaderBoard.objects.create(user_id=10, rating=5.7, date_time=datetime.datetime.now())
        command_for_refresh_view = Command()
        command_for_refresh_view.refresh_materialized_view()

    def test_response_players(self):
        response = self.client.get('/leaderboard/players')
        self.assertEqual(json.loads(response.content)['results'][0]['user_id'], 10)
        self.assertEqual(json.loads(response.content)['results'][0]['rating'], 5.7)
