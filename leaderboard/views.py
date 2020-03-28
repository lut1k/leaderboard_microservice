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
            self.queryset = LeaderBoard.objects.filter(position__lt=player_position)
        elif filter_field == 'after':
            self.queryset = LeaderBoard.objects.filter(position__gt=player_position)
        return self.queryset


class PlayerByIdAPIView(ListAPIView):
    serializer_class = LeaderBoardSerializer
    queryset = LeaderBoard.objects.all()

    def get_queryset(self):
        user_target = self.request.GET.getlist('user_id')
        queryset = LeaderBoard.objects.filter(user_id__in=user_target)
        return queryset


class PlayerAndNeighborsAPIView(ListAPIView):
    serializer_class = LeaderBoardSerializer
    queryset = LeaderBoard.objects.all()

    def get_queryset(self):
        user_target = self.request.GET.get('user_id')
        player_position_from_request = LeaderBoard.objects.filter(user_id=user_target).values()[0]['position']
        player_and_neighbor = LeaderBoard.objects.filter(position__range=(player_position_from_request - 1,
                                                                          player_position_from_request + 1,
                                                                          )
                                                         )
        return player_and_neighbor
