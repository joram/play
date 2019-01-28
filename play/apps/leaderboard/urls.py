from django.conf.urls import url
from apps.leaderboard import views
from util.routing import method_dispatch

urlpatterns = [
    url(r"^leaderboard/$", method_dispatch(GET=views.leaderboard.index)),
    url(r"^leaderboard/snakes/$", method_dispatch(GET=views.snakes.index)),
    url(
        r"^leaderboard/snakes/(?P<id>\w+)/$",
        method_dispatch(POST=views.snakes.create, DELETE=views.snakes.delete),
    ),
]
