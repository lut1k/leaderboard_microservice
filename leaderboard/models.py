from django.db import models


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
            print("Created user.") # TODO пилить отчет о сохранении.
        except:  # TODO обработать исключения, если user_id же существует.
            print("Key user_id already exists")
