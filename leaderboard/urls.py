from django.urls import path
from leaderboard.views import LeaderBoardAPIView, PlayerByIdAPIView, PlayerAndNeighborsAPIView

urlpatterns = [
    path('players', LeaderBoardAPIView.as_view(), name='players'),
    path('player-by-id', PlayerByIdAPIView.as_view(), name='player.by.id'),
    path('player-neighbors', PlayerAndNeighborsAPIView.as_view(), name='player.neighbors'),
]
