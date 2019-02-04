import csv
from urllib.parse import urlsplit

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect

from apps.authentication.decorators import admin_required
from apps.game.models import Game
from apps.tournament.forms import TournamentBracketForm
from apps.tournament.models import (
    Tournament,
    TournamentBracket,
    TournamentSnake,
    Heat,
    HeatGame,
    PreviousGameTiedException,
    DesiredGamesReachedValidationError,
    RoundNotCompleteException,
)


@admin_required
@login_required
@transaction.atomic
def new(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)

    if request.method == "POST":
        form = TournamentBracketForm(request.POST)

        if form.is_valid():
            bracket = form.save(commit=False)
            bracket.tournament = tournament
            bracket.save()

            # Save related sneks
            for snake in form.cleaned_data["snakes"]:
                # There has to be a tournament / snake relation, or its an error
                # (ie: can't add snake from outside the tournament)
                ts, _ = TournamentSnake.objects.get_or_create(
                    tournament=tournament, snake=snake
                )
                ts.bracket = bracket
                ts.save()

            messages.success(
                request, f'Tournament "{tournament.name}" successfully created'
            )
            return redirect("/tournaments/")
    else:
        form = TournamentBracketForm()
    return render(
        request, "tournament_bracket/new.html", {"form": form, "tournament": tournament}
    )


@admin_required
@login_required
def edit(request, bracket_id):
    tournament_bracket = TournamentBracket.objects.get(id=bracket_id)
    if request.method == "POST":
        form = TournamentBracketForm(request.POST, instance=tournament_bracket)

        if form.is_valid():
            bracket = form.save(commit=False)
            bracket.save()

            # Save related sneks
            for snake in form.cleaned_data["snakes"]:
                # There has to be a tournament / snake relation, or its an error
                # (ie: can't add snake from outside the tournament)
                ts, _ = TournamentSnake.objects.get_or_create(
                    tournament=tournament_bracket.tournament, snake=snake
                )
                ts.bracket = bracket
                ts.save()

            messages.success(
                request, f'Tournament Bracket "{tournament_bracket.name}" updated'
            )
            return redirect("/tournaments/")
    else:
        form = TournamentBracketForm(instance=tournament_bracket)

    return render(request, "tournament_bracket/edit.html", {"form": form})


@admin_required
@login_required
def show(request, id):
    tournament_bracket = TournamentBracket.objects.get(id=id)

    progression_details = []
    round = 1
    total_snakes = tournament_bracket.snakes.count()

    import math

    game_count = math.ceil(total_snakes / 8)
    snakes_per_game = total_snakes / game_count
    min_snakes_per_game = math.floor(snakes_per_game)
    max_snakes_per_game = math.ceil(snakes_per_game)
    snakes_advancing = game_count * 2

    snakes_per_game_msg = (
        f"{min_snakes_per_game}-{max_snakes_per_game}"
        if min_snakes_per_game != max_snakes_per_game
        else f"{min_snakes_per_game}"
    )
    while total_snakes > 8:
        progression_details.append(
            {
                "round": round,
                "num_games": game_count,
                "snakes_per_game": snakes_per_game_msg,
                "advancing": snakes_advancing,
            }
        )
        round += 1
        total_snakes = snakes_advancing

    progression_details.append(
        {
            "round": round,
            "num_games": game_count,
            "snakes_per_game": snakes_per_game_msg,
            "advancing": snakes_advancing,
        }
    )
    return render(
        request,
        "tournament_bracket/show.html",
        {"tournament_bracket": tournament_bracket, "progression": progression_details},
    )


@admin_required
@login_required
def show_csv(request, id):
    tournament_bracket = TournamentBracket.objects.get(id=id)
    # Create the HttpResponse object with the appropriate CSV header.
    filename = f"{tournament_bracket.tournament.name}_{tournament_bracket.name}.csv"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    for row in tournament_bracket.export():
        writer.writerow(row)

    return response


@admin_required
@login_required
def create_next_round(request, id):
    tournament_bracket = TournamentBracket.objects.get(id=id)
    try:
        tournament_bracket.create_next_round()
    except RoundNotCompleteException as e:
        messages.error(request, e.message)
    return redirect(f"/tournament/bracket/{id}")


@admin_required
@login_required
def update_game_statuses(request, bracket_id):
    bracket = TournamentBracket.objects.get(id=bracket_id)
    for heat in bracket.latest_round.heats:
        for hg in heat.games:
            if (
                hg.game.status == Game.Status.PENDING
                or hg.game.status == Game.Status.RUNNING
            ) and hg.game.engine_id is not None:
                hg.game.update_from_engine()
                hg.game.save()
    return redirect(f"/tournament/bracket/{bracket_id}")


@admin_required
@login_required
def create_game(request, id, heat_id):
    heat = Heat.objects.get(id=heat_id)
    try:
        heat.create_next_game()
    except PreviousGameTiedException:
        messages.error(request, "Previous game tied. It must be rerun")
    except DesiredGamesReachedValidationError:
        messages.error(request, "shouldn't create another game for this heat")
    except Exception as e:
        messages.error(request, e.__str__())
    return redirect(f"/tournament/bracket/{id}/")


@admin_required
@login_required
def delete_game(request, id, heat_id, heat_game_number):
    heat_game = HeatGame.objects.get(heat_id=heat_id, number=heat_game_number)
    heat_game.delete()
    return redirect(f"/tournament/bracket/{id}/")


@admin_required
@login_required
def run_game(request, id, heat_id, heat_game_number):
    heat_game = HeatGame.objects.get(heat_id=heat_id, number=heat_game_number)
    if heat_game.game is None or heat_game.game.engine_id is None:
        heat_game.game.create()
        heat_game.game.run()

    if "autoplay" in request.META["QUERY_STRING"]:
        return redirect(f"/games/{heat_game.game.engine_id}?autoplay=true")

    return redirect(f"/games/{heat_game.game.engine_id}")


@admin_required
@login_required
def tree(request, id):
    bracket = TournamentBracket.objects.get(id=id)
    context = {
        "bracket": bracket,
    }
    return render(request, "tournament_bracket/tree.html", context)


@admin_required
@login_required
def cast_tree(request, id):
    bracket = TournamentBracket.objects.get(id=id)
    split_url = urlsplit(request.build_absolute_uri())
    casting_uri = f"{split_url.scheme}://{split_url.netloc}/tournament/bracket/{id}/tree"
    bracket.tournament.casting_uri = casting_uri
    bracket.tournament.save()
    return redirect(f"/tournament/bracket/{id}/")
