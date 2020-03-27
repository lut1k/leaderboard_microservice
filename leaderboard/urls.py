from django.urls import path
from leaderboard.views import LeaderBoardAPIView

urlpatterns = [
    path('all_players', LeaderBoardAPIView.as_view(), name='all-players'),
]
