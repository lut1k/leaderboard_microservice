from django.db import models


class LeaderBoard(models.Model):
    class Meta:
        ordering = ('rating', 'date_time')

    user_id = models.IntegerField(unique=True)
    rating = models.FloatField()
    date_time = models.DateTimeField()

    def __str__(self):
        return "user_id--{}, rating--{}".format(self.user_id, self.rating)


class LeaderBoardView(models.Model):
    """
    Materialized View for relation LeaderBoard.
    View created bu query:
    "CREATE MATERIALIZED VIEW leaderboard_view AS
    SELECT row_number() OVER(ORDER BY rating DESC, date_time) AS position, user_id AS id, rating, date_time
    FROM leaderboard_leaderboard;".
    """
    position = models.BigIntegerField()
    id = models.IntegerField(primary_key=True)
    rating = models.FloatField()
    date_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'leaderboard_view'
