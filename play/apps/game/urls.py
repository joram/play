from django.conf.urls import url
from apps.game import views
from util.routing import method_dispatch

urlpatterns = [
    url(r'^games/$', method_dispatch(
        GET=views.games.index,
        POST=views.games.create,
    )),
    url(r'^games/new/$', method_dispatch(
        GET=views.games.new,
    )),
    url(r'^games/(?P<id>.+)/$', method_dispatch(
        GET=views.games.show,
    ))
]