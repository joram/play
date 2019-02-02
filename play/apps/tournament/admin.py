from django.contrib import admin
from apps.tournament.models import Team


class TeamAdmin(admin.ModelAdmin):
    search_fields = ["name"]


admin.site.register(Team, TeamAdmin)
