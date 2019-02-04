from django.urls import path
from apps.platform.views import player
from util.routing import method_dispatch as route

urlpatterns = [
    path(
        "profile",
        route(GET=player.edit, PUT=player.update, DELETE=player.delete),
        name="profile",
    )
]
