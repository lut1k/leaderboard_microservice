from django.db import models


class LeaderBoard(models.Model):
    """
    The model is a leaderboard.
    """
    user_id = models.IntegerField(unique=True)
    rating = models.FloatField()
    date_time = models.DateTimeField()
    position = models.IntegerField(default=0)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return "user_id--{}, rating--{}".format(self.user_id, self.rating)

    class Meta:
        ordering = ['rating', '-date_time']
