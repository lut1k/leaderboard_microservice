from django.db import models, IntegrityError


class LeaderBoard(models.Model):
    class Meta:
        ordering = ['position', '-date_time']

    user_id = models.IntegerField(unique=True)
    rating = models.FloatField()
    date_time = models.DateTimeField()
    position = models.IntegerField(default=0)

    def __str__(self):
        return "user_id--{}, rating--{}".format(self.user_id, self.rating)

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
            # TODO каким образом уведомлять о сохранении? И надо ли.
            print("Created user with user_id <{}>.".format(self.user_id))
        except IntegrityError:
            print("user_id - {} is all ready exist".format(self.user_id))
