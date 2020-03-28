from django.contrib import admin
from leaderboard.models import LeaderBoard


class LeaderBoardAdmin(admin.ModelAdmin):
    list_display = ['position', 'rating', 'user_id', 'date_time']
    ordering = ['user_id']
    list_filter = ['rating']
    search_fields = ['user_id']


admin.site.register(LeaderBoard, LeaderBoardAdmin)
