from django.conf.urls import url
from apps.tournament import views as tournament_views
from util.routing import method_dispatch

urlpatterns = [
    url(r'^team/$', method_dispatch(
        GET=tournament_views.team.index,
        PUT=tournament_views.team.update,
    )),
    url(r'^team/new/$', method_dispatch(
        GET=tournament_views.team.new,
        POST=tournament_views.team.new,
    )),
    url(r'^team/edit/$', method_dispatch(
        GET=tournament_views.team.edit,
    )),
    url(r'^team/members/$', method_dispatch(
        GET=tournament_views.members.index,
    )),
    url(r'^team/members/new/$', method_dispatch(
        GET=tournament_views.members.new,
        POST=tournament_views.members.new,
    )),
    url(r'^team/members/(?P<id>\w+)/$', method_dispatch(
        DELETE=tournament_views.members.delete,
    )),
    url(r'^tournament/bracket/new/$', method_dispatch(
        GET=tournament_views.tournament_bracket.new,
        POST=tournament_views.tournament_bracket.new,
    )),
    url(r'^tournament/bracket/(?P<id>\w+)/edit/$', method_dispatch(
        GET=tournament_views.tournament_bracket.edit,
        POST=tournament_views.tournament_bracket.edit,
        PUT=tournament_views.tournament_bracket.edit,
    )),
    url(r'^tournament/bracket/(?P<id>\w+)/add/snake$', method_dispatch(
        GET=tournament_views.tournament_bracket_snake.new,
        POST=tournament_views.tournament_bracket_snake.new,
        PUT=tournament_views.tournament_bracket_snake.new,
    )),
    url(r'^tournament/bracket/(?P<id>\w+)/$', method_dispatch(
        GET=tournament_views.tournament_bracket.show,
    )),
    url(r'^tournament/bracket/(?P<id>\w+)/current_game$', method_dispatch(
        GET=tournament_views.tournament_bracket.show_current_game,
    )),
    url(r'^tournament/bracket/(?P<id>\w+)/create/next/round$', method_dispatch(
        GET=tournament_views.tournament_bracket.create_next_round,
    )),
    url(r'^tournament/bracket/(?P<id>\w+)/heat/(?P<heat_id>\w+)/create_game/$', method_dispatch(
        GET=tournament_views.tournament_bracket.create_game,
        POST=tournament_views.tournament_bracket.create_game,
    )),
    url(r'^tournament/bracket/(?P<id>\w+)/heat/(?P<heat_id>\w+)/game/(?P<heat_game_number>\w+)/$', method_dispatch(
        GET=tournament_views.tournament_bracket.run_game,
    )),
    url(r'^tournaments/$', method_dispatch(
        GET=tournament_views.tournament.index,
    )),
    url(r'^tournament/new/$', method_dispatch(
        GET=tournament_views.tournament.new,
        POST=tournament_views.tournament.new,
    )),
    url(r'^tournament/(?P<id>\w+)/edit/$', method_dispatch(
        GET=tournament_views.tournament.edit,
        POST=tournament_views.tournament.edit,
    )),
]
