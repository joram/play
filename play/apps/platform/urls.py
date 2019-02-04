from django.conf.urls import url
from apps.platform.views import player, players
from util.routing import method_dispatch as route

urlpatterns = [
    url(
        r"^profile/$",
        route(GET=player.edit, PUT=player.update, DELETE=player.delete),
        name="profile",
    ),
    url(r"^players/(?P<username>[\w\-]+)/$", route(GET=players.show), name="player"),
]
