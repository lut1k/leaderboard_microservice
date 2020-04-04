from django.http import Http404
from django.shortcuts import get_list_or_404
from rest_framework.generics import ListAPIView
from leaderboard.models import LeaderBoardView
from leaderboard.pagination import PageNumberPagination
from leaderboard.serializers import LeaderBoardSerializer


class LeaderBoardAPIView(ListAPIView):
    queryset = LeaderBoardView.objects.all()
    serializer_class = LeaderBoardSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        player_position = self.request.GET.get('position')
        filter_field = self.request.GET.get('filter')
        filter_dict = {
            filter_field: player_position,
        }
        if filter_field:
            return get_list_or_404(LeaderBoardView, **filter_dict)
        return super().get_queryset()


class PlayerByIdAPIView(ListAPIView):
    serializer_class = LeaderBoardSerializer
    queryset = LeaderBoardView.objects.all()

    def get_queryset(self):
        user_target = self.request.GET.getlist('user_id')
        queryset = get_list_or_404(LeaderBoardView, id__in=user_target)
        return queryset


class PlayerAndNeighborsAPIView(ListAPIView):
    serializer_class = LeaderBoardSerializer
    queryset = LeaderBoardView.objects.all()

    def get_queryset(self):
        user_target = self.request.GET.get('user_id')
        player_from_request = LeaderBoardView.objects.filter(id=user_target)
        if len(player_from_request) == 1:
            player_position_from_request = player_from_request.values()[0]['position']
            player_and_neighbor = LeaderBoardView.objects.filter(position__range=(player_position_from_request - 1,
                                                                                  player_position_from_request + 1,
                                                                                  )
                                                                 )
            return player_and_neighbor
        raise Http404()
