from django.shortcuts import get_list_or_404
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
        filter_dict = {
            filter_field: player_position,
        }
        if filter_field:
            return get_list_or_404(LeaderBoard, **filter_dict)
        return super().get_queryset()


class PlayerByIdAPIView(ListAPIView):
    serializer_class = LeaderBoardSerializer
    queryset = LeaderBoard.objects.all()

    def get_queryset(self):
        user_target = self.request.GET.getlist('user_id')
        queryset = get_list_or_404(LeaderBoard, user_id__in=user_target)
        return queryset


class PlayerAndNeighborsAPIView(ListAPIView):
    serializer_class = LeaderBoardSerializer
    queryset = LeaderBoard.objects.all()

    # TODO реализовать через один запрос.
    def get_queryset(self):
        user_target = self.request.GET.get('user_id')
        player_position_from_request = LeaderBoard.objects.filter(user_id=user_target).values()[0]['position']
        player_and_neighbor = LeaderBoard.objects.filter(position__range=(player_position_from_request - 1,
                                                                          player_position_from_request + 1,
                                                                          )
                                                         )
        return player_and_neighbor
