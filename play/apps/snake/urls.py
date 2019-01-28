from django.conf.urls import url
from apps.snake import views
from util.routing import method_dispatch

urlpatterns = [
    url(
        r"^snakes/$",
        method_dispatch(GET=views.snakes.index, POST=views.snakes.create),
        name="snakes",
    ),
    url(r"^snakes/new/$", method_dispatch(GET=views.snakes.new), name="snakes_new"),
    url(
        r"^snakes/(?P<id>\w+)/$",
        method_dispatch(DELETE=views.snakes.delete, PUT=views.snakes.update),
        name="snakes_show",
    ),
    url(
        r"^snakes/(?P<id>\w+)/edit/$",
        method_dispatch(GET=views.snakes.edit),
        name="snakes_edit",
    ),
]
