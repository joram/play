from django.conf.urls import url
from apps.game import views
from util.routing import method_dispatch

urlpatterns = [
    url(r"^games/$", method_dispatch(GET=views.games.index), name="games"),
    url(
        r"^games/new/$",
        method_dispatch(GET=views.games.new, POST=views.games.new),
        name="games_new",
    ),
    url(
        r"^games/(?P<id>.+)/$", method_dispatch(GET=views.games.show), name="games_show"
    ),
]
