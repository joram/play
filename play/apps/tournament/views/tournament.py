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
    if request.GET.get("json") == "true":
        return JsonResponse({"tournament": {"casting_uri": tournament.casting_uri}})

    return render(
        request, "tournament/show_current_game.html", {"tournament": tournament}
    )


@admin_required
@login_required
@transaction.atomic
def cast_current_game(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    heat_game = HeatGame.objects.get(id=request.POST.get("heat_game_id"))

    if heat_game.game is None or heat_game.game.engine_id is None:
        heat_game.game.create()
        heat_game.game.run()

    tournament.casting_uri = (
        generate_game_url(heat_game.game.engine_id) + "&autoplay=true&countdown=10"
    )
    tournament.save()

    # flag previously watching games as watched
    rounds = Round.objects.filter(tournament_bracket__in=tournament.brackets)
    heats = Heat.objects.filter(round__in=rounds)
    HeatGame.objects.filter(heat__in=heats, status=HeatGame.WATCHING).update(status=HeatGame.WATCHED)

    heat_game.status = HeatGame.WATCHING
    heat_game.save()

    heat_games = HeatGame.objects.filter(heat__in=heats)
    return JsonResponse(
        {
            "heat_games": [
                {"id": hg.id, "status": hg.human_readable_status} for hg in heat_games
            ]
        }
    )
