from django.conf.urls import url
from apps.tournament import views as tournament_views
from util.routing import method_dispatch

urlpatterns = [
    url(
        r"^team/$",
        method_dispatch(
            GET=tournament_views.team.index, PUT=tournament_views.team.update
        ),
    ),
    url(
        r"^team/new/$",
        method_dispatch(GET=tournament_views.team.new, POST=tournament_views.team.new),
    ),
    url(r"^team/edit/$", method_dispatch(GET=tournament_views.team.edit)),
    url(r"^team/members/$", method_dispatch(GET=tournament_views.members.index)),
    url(
        r"^team/members/new/$",
        method_dispatch(
            GET=tournament_views.members.new, POST=tournament_views.members.new
        ),
    ),
    url(
        r"^team/members/(?P<id>\w+)/$",
        method_dispatch(DELETE=tournament_views.members.delete),
    ),
    url(
        r"^tournament/(?P<tournament_id>\w+)/bracket/new/$",
        method_dispatch(
            GET=tournament_views.tournament_bracket.new,
            POST=tournament_views.tournament_bracket.new,
        ),
    ),
    url(
        r"^tournament/bracket/(?P<bracket_id>\w+)/edit/$",
        method_dispatch(
            GET=tournament_views.tournament_bracket.edit,
            POST=tournament_views.tournament_bracket.edit,
            PUT=tournament_views.tournament_bracket.edit,
        ),
    ),
    url(
        r"^tournament/(?P<tournament_id>\w+)/compete$",
        method_dispatch(
            GET=tournament_views.tournament_snake.compete,
            POST=tournament_views.tournament_snake.compete,
            PUT=tournament_views.tournament_snake.compete,
        ),
    ),
    url(
        r"^tournament/snake/(?P<tournament_snake_id>\w+)/edit",
        method_dispatch(
            GET=tournament_views.tournament_snake.edit,
            POST=tournament_views.tournament_snake.edit,
            PUT=tournament_views.tournament_snake.edit,
        ),
    ),
    url(
        r"^tournament/snake/(?P<tournament_snake_id>\w+)/delete",
        method_dispatch(
            GET=tournament_views.tournament_snake.delete,
            POST=tournament_views.tournament_snake.delete,
            PUT=tournament_views.tournament_snake.delete,
        ),
    ),
    url(
        r"^tournament/bracket/(?P<id>\w+)/$",
        method_dispatch(GET=tournament_views.tournament_bracket.show),
    ),
    url(
        r"^tournament/bracket/(?P<id>\w+)/csv$",
        method_dispatch(GET=tournament_views.tournament_bracket.show_csv),
    ),
    url(
        r"^tournament/bracket/(?P<id>\w+)/tree$",
        method_dispatch(GET=tournament_views.tournament_bracket.tree),
    ),
    url(
        r"^tournament/bracket/(?P<id>\w+)/set-casting",
        method_dispatch(GET=tournament_views.tournament_bracket.cast_page),
    ),
    url(
        r"^tournament/bracket/(?P<id>\w+)/create/next/round$",
        method_dispatch(GET=tournament_views.tournament_bracket.create_next_round),
    ),
    url(
        r"^tournament/bracket/(?P<bracket_id>\w+)/update/games",
        method_dispatch(GET=tournament_views.tournament_bracket.update_game_statuses),
    ),
    url(
        r"^tournament/bracket/(?P<id>\w+)/heat/(?P<heat_id>\w+)/create_game/$",
        method_dispatch(
            GET=tournament_views.tournament_bracket.create_game,
            POST=tournament_views.tournament_bracket.create_game,
        ),
    ),
    url(
        r"^tournament/bracket/(?P<id>\w+)/heat/(?P<heat_id>\w+)/game/(?P<heat_game_number>\w+)/$",
        method_dispatch(GET=tournament_views.tournament_bracket.run_game),
    ),
    url(
        r"^tournament/bracket/(?P<id>\w+)/heat/(?P<heat_id>\w+)/game/(?P<heat_game_number>\w+)/delete",
        method_dispatch(GET=tournament_views.tournament_bracket.delete_game),
    ),
    url(r"^tournaments/$", method_dispatch(GET=tournament_views.tournament.index)),
    url(
        r"^tournament/new/$",
        method_dispatch(
            GET=tournament_views.tournament.new, POST=tournament_views.tournament.new
        ),
    ),
    url(
        r"^tournament/(?P<id>\w+)/edit/$",
        method_dispatch(
            GET=tournament_views.tournament.edit, POST=tournament_views.tournament.edit
        ),
    ),
    url(
        r"^tournament/(?P<tournament_id>\w+)/current_game$",
        method_dispatch(
            GET=tournament_views.tournament.show_current_game,
            POST=tournament_views.tournament.cast_current_game,
        ),
    ),
]
