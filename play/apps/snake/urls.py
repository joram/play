from django.conf.urls import url
from apps.snake import views
from util.routing import method_dispatch

urlpatterns = [
    url(r'^snakes/$', method_dispatch(
        GET=views.snakes.index,
        POST=views.snakes.create,
    )),
    url(r'^snakes/new/$', method_dispatch(
        GET=views.snakes.new,
    )),
    url(r'^snakes/(?P<id>\w+)/$', method_dispatch(
        DELETE=views.snakes.delete,
        PUT=views.snakes.update,
    )),
    url(r'^snakes/(?P<id>\w+)/edit/$', method_dispatch(
        GET=views.snakes.edit,
    )),
]
