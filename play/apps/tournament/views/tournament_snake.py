from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect

from apps.tournament.forms import TournamentSnakeForm
from apps.tournament.models import Tournament, TournamentSnake, Snake, TournamentBracket


@login_required
@transaction.atomic
def compete(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)

    if request.method == "POST":
        snake = Snake.objects.get(id=request.POST.get("snake"))
        bracket = TournamentBracket.objects.get(id=request.POST.get("bracket"))
        form = TournamentSnakeForm(
            user=request.user, tournament=tournament, snake=snake, bracket=bracket
        )
        form.bracket = TournamentBracket.objects.get(id=request.POST.get("bracket"))
        if form.is_valid():
            ts = form.save()
            messages.success(
                request,
                f"added {ts.snake.name} to bracket {ts.bracket.name} in {ts.tournament.name}",
            )
            return redirect("/team/")
        # failed
        return redirect("/team/")

    form = TournamentSnakeForm(
        user=request.user, tournament=tournament, snake=None, bracket=None
    )

    return render(request, "tournament_snake/new.html", {"form": form})


@login_required
@transaction.atomic
def edit(request, tournament_snake_id):
    ts = TournamentSnake.objects.get(id=tournament_snake_id)
    if request.method == "POST":
        snake = Snake.objects.get(id=request.POST.get("snake"))
        form = TournamentSnakeForm(
            user=request.user, tournament=ts.tournament, snake=snake, bracket=ts.bracket
        )
        form.bracket = TournamentBracket.objects.get(id=request.POST.get("bracket"))
        if form.is_valid():
            old_ts = ts
            ts = form.save()
            if ts.snake != old_ts.snake:
                messages.success(
                    request,
                    f"switched snake from  {old_ts.snake.name} to {ts.snake.name}",
                )
            if ts.bracket != old_ts.bracket:
                messages.success(
                    request,
                    f"switched bracket from  {old_ts.bracket.name} to {ts.bracket.name}",
                )
            return redirect("/team/")
        messages.error(request, "Tournament in a non-modifiable state.")
        return redirect("/team/")

    form = TournamentSnakeForm(
        user=request.user, tournament=ts.tournament, snake=ts.snake, bracket=ts.bracket
    )
    form.snake = ts.snake
    return render(request, "tournament_snake/edit.html", {"form": form})


@login_required
@transaction.atomic
def delete(request, tournament_snake_id):
    ts = TournamentSnake.objects.get(id=tournament_snake_id)
    ts.delete()
    messages.success(
        request,
        f"removed {ts.snake.name} from bracket {ts.bracket.name} in {ts.tournament.name}",
    )
    return redirect("/team/")
