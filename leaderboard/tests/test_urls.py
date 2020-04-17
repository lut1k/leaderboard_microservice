from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase


class URLPatternsTest(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('leaderboard/', include('leaderboard.urls')),
    ]

    def test_url_players(self):
        url = reverse('players')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data['results'], [])

    def test_url_players_by_id(self):
        url = reverse('player.by.id')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_url_player_neighbors(self):
        url = reverse('player.neighbors')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
