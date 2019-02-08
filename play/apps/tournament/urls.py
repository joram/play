from django.urls import re_path
from apps.tournament import views as tournament_views
from util.routing import method_dispatch as route

urlpatterns = [
    re_path(
        r"^team/$",
        route(GET=tournament_views.team.index, PUT=tournament_views.team.update),
    ),
    re_path(
        r"^team/new/$",
        route(GET=tournament_views.team.new, POST=tournament_views.team.new),
    ),
    re_path(r"^team/edit/$", route(GET=tournament_views.team.edit)),
    re_path(r"^team/members/$", route(GET=tournament_views.members.index)),
    re_path(
        r"^team/members/new/$",
        route(GET=tournament_views.members.new, POST=tournament_views.members.new),
    ),
    re_path(
        r"^team/members/(?P<id>\w+)/$", route(DELETE=tournament_views.members.delete)
    ),
    re_path(
        r"^tournament/(?P<tournament_id>\w+)/bracket/new/$",
        route(
            GET=tournament_views.tournament_bracket.new,
            POST=tournament_views.tournament_bracket.new,
        ),
    ),
    re_path(
        r"^tournament/bracket/(?P<bracket_id>\w+)/edit/$",
        route(
            GET=tournament_views.tournament_bracket.edit,
            POST=tournament_views.tournament_bracket.edit,
            PUT=tournament_views.tournament_bracket.edit,
        ),
    ),
    re_path(
        r"^tournament/(?P<tournament_id>\w+)/compete$",
        route(
            GET=tournament_views.tournament_snake.compete,
            POST=tournament_views.tournament_snake.compete,
            PUT=tournament_views.tournament_snake.compete,
        ),
    ),
    re_path(
        r"^tournament/snake/(?P<tournament_snake_id>\w+)/edit",
        route(
            GET=tournament_views.tournament_snake.edit,
            POST=tournament_views.tournament_snake.edit,
            PUT=tournament_views.tournament_snake.edit,
        ),
    ),
    re_path(
        r"^tournament/snake/(?P<tournament_snake_id>\w+)/delete",
        route(
            GET=tournament_views.tournament_snake.delete,
            POST=tournament_views.tournament_snake.delete,
            PUT=tournament_views.tournament_snake.delete,
        ),
    ),
    re_path(
        r"^tournament/bracket/(?P<id>\w+)/$",
        route(GET=tournament_views.tournament_bracket.show),
    ),
    re_path(
        r"^tournament/bracket/(?P<id>\w+)/csv$",
        route(GET=tournament_views.tournament_bracket.show_csv),
    ),
    re_path(
        r"^tournament/bracket/(?P<id>\w+)/tree$",
        route(GET=tournament_views.tournament_bracket.tree),
    ),
    re_path(
        r"^tournament/bracket/(?P<id>\w+)/set-casting",
        route(GET=tournament_views.tournament_bracket.cast_page),
    ),
    re_path(
        r"^tournament/bracket/(?P<id>\w+)/create/next/round$",
        route(GET=tournament_views.tournament_bracket.create_next_round),
    ),
    re_path(
        r"^tournament/bracket/(?P<bracket_id>\w+)/update/games",
        route(GET=tournament_views.tournament_bracket.update_game_statuses),
    ),
    re_path(
        r"^tournament/bracket/(?P<id>\w+)/heat/(?P<heat_id>\w+)/create_game/$",
        route(
            GET=tournament_views.tournament_bracket.create_game,
            POST=tournament_views.tournament_bracket.create_game,
        ),
    ),
    re_path(
        r"^tournament/bracket/(?P<id>\w+)/heat/(?P<heat_id>\w+)/game/(?P<heat_game_number>\w+)/$",
        route(GET=tournament_views.tournament_bracket.run_game),
    ),
    re_path(
        r"^tournament/bracket/(?P<id>\w+)/heat/(?P<heat_id>\w+)/game/(?P<heat_game_number>\w+)/delete",
        route(GET=tournament_views.tournament_bracket.delete_game),
    ),
    re_path(r"^tournaments/$", route(GET=tournament_views.tournament.index)),
    re_path(
        r"^tournament/new/$",
        route(
            GET=tournament_views.tournament.new, POST=tournament_views.tournament.new
        ),
    ),
    re_path(
        r"^tournament/(?P<id>\w+)/edit/$",
        route(
            GET=tournament_views.tournament.edit, POST=tournament_views.tournament.edit
        ),
    ),
    re_path(
        r"^tournament/(?P<tournament_id>\w+)/current_game$",
        route(
            GET=tournament_views.tournament.show_current_game,
            POST=tournament_views.tournament.cast_current_game,
        ),
    ),
    re_path(
        r"^tournament/(?P<tournament_id>\w+)/commentator",
        route(GET=tournament_views.tournament.commentator_details),
    ),
]
