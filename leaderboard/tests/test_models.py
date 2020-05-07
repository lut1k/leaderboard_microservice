import random

from django.test import TestCase
import datetime
from leaderboard.management.commands.refresh_leaderboardview import Command
from leaderboard.models import LeaderBoard, LeaderBoardView


class ModelLeaderBoardTest(TestCase):
    """ Test module for LeaderBoard model """

    @classmethod
    def setUpTestData(cls):
        LeaderBoard.objects.create(user_id=10, rating=7.7, date_time=datetime.datetime.now())

    def test_rating_label(self):
        user = LeaderBoard.objects.get(user_id=10)
        field_label = user._meta.get_field('rating').verbose_name
        self.assertEquals(field_label, 'rating')

    def test_str_method(self):
        user = LeaderBoard.objects.get(user_id=10)
        expected_str = "user_id--{}, rating--{}".format(user.user_id, user.rating)
        self.assertEqual(expected_str, str(user))


class LeaderBoardViewTest(TestCase):
    """ Test module for LeaderBoardView model """

    @classmethod
    def setUpTestData(cls):
        for player in range(10):
            LeaderBoard.objects.create(user_id=random.randint(1, 300000),
                                       rating=round(random.uniform(1, 100), 1),
                                       date_time=datetime.datetime.now()
                                       )
        command_for_refresh_view = Command()
        command_for_refresh_view.refresh_materialized_view()

    def test_positions_user(self):
        ordered_users_from_leaderboard = LeaderBoard.objects.order_by('-rating', 'date_time')
        user_id_with_first_position = ordered_users_from_leaderboard.first().user_id
        user_id_with_last_position = ordered_users_from_leaderboard.last().user_id

        users_from_leaderboard_view = LeaderBoardView.objects.order_by('-rating', 'date_time')
        first_position_from_leaderboardview = users_from_leaderboard_view.first().user_id
        last_position_from_leaderboardview = users_from_leaderboard_view.last().user_id

        self.assertEqual(first_position_from_leaderboardview, user_id_with_first_position)
        self.assertEqual(last_position_from_leaderboardview, user_id_with_last_position)
