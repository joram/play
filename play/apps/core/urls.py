from django.conf.urls import url
from django.urls import path

from apps.core.views import profile, profiles, snake, game
from util.routing import method_dispatch as route

urlpatterns = [
    url(
        r"^profile/$",
        route(GET=profile.edit, PUT=profile.update, DELETE=profile.delete),
        name="profile",
    ),
    url(r"^u/(?P<username>[\w\-]+)/$", route(GET=profiles.show), name="u"),
    path("s/new/", route(GET=snake.new, POST=snake.create)),
    path("s/<snake_id>/", route(GET=snake.show, DELETE=snake.delete)),
    path("s/<snake_id>/edit/", route(GET=snake.edit, PUT=snake.update)),
    path("g/new/", route(GET=game.new, POST=game.create)),
    path("g/<game_id>", route(GET=game.show)),
    path("g/snake-autocomplete/", route(GET=game.snake_autocomplete)),
    path("g/snake-info/", route(GET=game.snake_info)),
]
