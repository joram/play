from django.conf.urls import url
from apps.tournament import views as tournament_views
from util.routing import method_dispatch

urlpatterns = [
    url(r'^team/$', method_dispatch(
        GET=tournament_views.team.index,
        POST=tournament_views.team.create,
        PUT=tournament_views.team.update,
    )),
    url(r'^team/new/$', method_dispatch(
        GET=tournament_views.team.new,
    )),
    url(r'^team/edit/$', method_dispatch(
        GET=tournament_views.team.edit,
    )),
    url(r'^team/members/$', method_dispatch(
        GET=tournament_views.members.index,
        POST=tournament_views.members.create,
    )),
    url(r'^team/members/new/$', method_dispatch(
        GET=tournament_views.members.new,
    )),
    url(r'^team/members/(?P<id>\w+)/$', method_dispatch(
        DELETE=tournament_views.members.delete,
    )),
]
