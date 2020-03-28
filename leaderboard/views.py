from rest_framework.generics import ListAPIView
from leaderboard.models import LeaderBoard
from leaderboard.pagination import PageNumberPagination
from leaderboard.serializers import LeaderBoardSerializer


class LeaderBoardAPIView(ListAPIView):
    queryset = LeaderBoard.objects.all()
    serializer_class = LeaderBoardSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        player_position = self.request.GET.get('position')
        filter_field = self.request.GET.get('filter')
        if filter_field == 'before':
            queryset = LeaderBoard.objects.filter(position__lt=player_position)
            return queryset
        elif filter_field == 'after':
            queryset = LeaderBoard.objects.filter(position__gt=player_position)
            return queryset
        return super().get_queryset()
