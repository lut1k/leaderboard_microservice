from django.contrib import admin
from leaderboard.models import LeaderBoard


class LeaderBoardAdmin(admin.ModelAdmin):
    list_display = ['rating', 'user_id', 'date_time']
    ordering = ['rating']
    list_filter = ['rating']
    search_fields = ['user_id']


admin.site.register(LeaderBoard, LeaderBoardAdmin)
