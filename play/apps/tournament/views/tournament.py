from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect

from apps.authentication.decorators import admin_required
from apps.tournament.forms import TournamentForm
from apps.tournament.models import Tournament, TournamentBracket, Heat, HeatGame, Round
from apps.utils.helpers import generate_game_url


@admin_required
@login_required
def index(request):
    user = request.user
    return render(
        request,
        "tournament/list.html",
        {
            "tournaments": Tournament.objects.all(),
            "tournament_brackets": TournamentBracket.objects.all(),
            "user": user,
        },
    )


@admin_required
@login_required
@transaction.atomic
def new(request):
    if request.method == "POST":
        form = TournamentForm(request.POST)

        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.save()
            messages.success(
                request, f'Tournament "{tournament.name}" successfully created'
            )
            return redirect("/tournaments/")
    else:
        form = TournamentForm(initial={"date": datetime.now()})

    return render(request, "tournament/new.html", {"form": form})


@admin_required
@login_required
@transaction.atomic
def edit(request, id):
    tournament = Tournament.objects.get(id=id)
    if request.method == "POST":
        form = TournamentForm(request.POST, instance=tournament)

        if form.is_valid():
            t = form.save(commit=False)
            t.save()

            messages.success(request, f'Tournament group "{tournament.name}" updated')
            return redirect("/tournaments/")
    else:
        form = TournamentForm(instance=tournament)

    return render(request, "tournament/edit.html", {"form": form})


@admin_required
@login_required
def show_current_game(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    rounds = Round.objects.filter(tournament_bracket__in=tournament.brackets)
    heats = Heat.objects.filter(round__in=rounds)
    heat_games = HeatGame.objects.filter(heat__in=heats)
    heat_game = heat_games.filter(status=HeatGame.WATCHING)
    if request.GET.get("json") == "true":
        if not heat_game.exists():
            return JsonResponse({"heat_game": {"game": {"id": -1}}})

        heat_game = heat_game[0]
        return JsonResponse(
            {
                "heat_game": {
                    # "status": heat_game.status,
                    "number": heat_game.number,
                    "heat": {
                        "id": heat_game.heat.id,
                        "number": heat_game.heat.number,
                        "round": {
                            "id": heat_game.heat.round.id,
                            "number": heat_game.heat.round.number,
                            "bracket": {
                                "id": heat_game.heat.round.tournament_bracket.id,
                                "name": heat_game.heat.round.tournament_bracket.name,
                                "tournament": {
                                    "id": heat_game.heat.round.tournament_bracket.tournament.id,
                                    "name": heat_game.heat.round.tournament_bracket.tournament.name,
                                },
                            },
                        },
                    },
                    "game": {
                        "id": heat_game.game.id,
                        "engine_id": heat_game.game.engine_id,
                        "url": generate_game_url(heat_game.game.engine_id),
                    },
                }
            }
        )

    return render(
        request,
        "tournament/show_current_game.html",
        {"heat_game": heat_game, "tournament": tournament},
    )


@admin_required
@login_required
@transaction.atomic
def set_current_game(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    rounds = Round.objects.filter(tournament_bracket__in=tournament.brackets)
    heats = Heat.objects.filter(round__in=rounds)
    heat_games = HeatGame.objects.filter(heat__in=heats)

    heat_game = heat_games.filter(status=HeatGame.WATCHING)
    if not heat_game.exists():
        # problem
        pass

    watch_heat_game = heat_games.filter(id=request.POST.get("heat_game_id"))
    if not watch_heat_game.exists():
        # problem
        pass

    heat_game.update(status=HeatGame.WATCHED)

    if watch_heat_game[0].game is None or watch_heat_game[0].game.engine_id is None:
        watch_heat_game[0].game.create()
        watch_heat_game[0].game.run()
    watch_heat_game.update(status=HeatGame.WATCHING)

    heat_games = HeatGame.objects.filter(heat__in=heats)
    return JsonResponse(
        {
            "heat_games": [
                {"id": hg.id, "status": hg.human_readable_status} for hg in heat_games
            ]
        }
    )
