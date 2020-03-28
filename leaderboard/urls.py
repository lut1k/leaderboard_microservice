from django.urls import path
from leaderboard.views import LeaderBoardAPIView

urlpatterns = [
    path('players', LeaderBoardAPIView.as_view(), name='players'),
]
