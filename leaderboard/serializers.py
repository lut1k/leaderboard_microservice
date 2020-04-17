from rest_framework import serializers
from leaderboard.models import LeaderBoardView


class LeaderBoardSerializer(serializers.ModelSerializer):
    """Class serializes model LeaderBoardView"""
    class Meta:
        model = LeaderBoardView
        fields = ('position', 'user_id', 'rating')
