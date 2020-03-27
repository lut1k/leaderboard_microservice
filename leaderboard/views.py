from rest_framework.generics import ListAPIView
from leaderboard.models import LeaderBoard
from leaderboard.pagination import CustomPagination
from leaderboard.serializers import LeaderBoardSerializer


class LeaderBoardAPIView(ListAPIView):
    queryset = LeaderBoard.objects.all()
    serializer_class = LeaderBoardSerializer
    pagination_class = CustomPagination
