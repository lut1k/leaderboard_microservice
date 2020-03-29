from rest_framework import serializers
from leaderboard.models import LeaderBoard


class LeaderBoardSerializer(serializers.ModelSerializer):
    """Class serializes model LeaderBoard"""
    class Meta:
        model = LeaderBoard
        fields = ("user_id", "rating", "position")
