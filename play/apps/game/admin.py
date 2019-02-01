from django.contrib import admin
from apps.game.models import Game


class GameAdmin(admin.ModelAdmin):
    pass


admin.site.register(Game, GameAdmin)
