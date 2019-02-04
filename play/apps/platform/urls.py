from django.urls import path
from apps.platform.views import player, players
from util.routing import method_dispatch as route

urlpatterns = [
    path(
        "profile",
        route(GET=player.edit, PUT=player.update, DELETE=player.delete),
        name="profile",
    ),
    path("players/<username>", route(GET=players.show), name="player"),
]
