from rest_framework import serializers
from leaderboard.models import LeaderBoard, LeaderBoardView


class LeaderBoardSerializer(serializers.ModelSerializer):
    """Class serializes model LeaderBoardView"""
    class Meta:
        model = LeaderBoardView
        fields = ('position', 'id', 'rating')
