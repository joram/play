from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse

from apps.tournament.forms import TournamentForm
from apps.tournament.models import Tournament, TournamentBracket, TournamentSnake, Heat, HeatGame, Round
from apps.authentication.decorators import admin_required
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
            for snake in form.cleaned_data["snakes"]:
                ts = TournamentSnake(tournament=tournament, snake=snake)
                ts.save()
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
            ts = TournamentSnake.objects.filter(tournament=tournament)

            # Remove snakes from the tournament
            snake_ids = [s.id for s in form.cleaned_data["snakes"]]
            for remove in ts.exclude(snake_id__in=snake_ids):
                remove.delete()

            # Add new snakes
            ts_ids = ts.values_list("snake__pk", flat=True)
            for snake in form.cleaned_data["snakes"]:
                if snake.id not in ts_ids:
                    ts = TournamentSnake(tournament=tournament, snake=snake)
                    ts.save()

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
    # heat_game = heat_games.filter(status=HeatGame.WATCHING)
    heat_game = heat_games[0]

    if request.GET.get("json") == "true":
        if True: #heat_game.exists():
            # heat_game = heat_game[0]
            return JsonResponse({"heat_game": {
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
                    "url": generate_game_url(heat_game.game.id),
                },
            }})

    return render(
        request,
        "tournament/show_current_game.html",
        {"heat_game": heat_game},
    )
