from django.conf.urls import url
from django.urls import path

from apps.core.views import profile, profiles, snake
from util.routing import method_dispatch as route

urlpatterns = [
    url(
        r"^profile/$",
        route(GET=profile.edit, PUT=profile.update, DELETE=profile.delete),
        name="profile",
    ),
    url(r"^u/(?P<username>[\w\-]+)/$", route(GET=profiles.show), name="u"),
    path("s/new/", snake.create),
    path("s/<snake_id>/", snake.index),
]
