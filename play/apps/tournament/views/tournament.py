from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.tournament.forms import TournamentForm
from apps.tournament.models import Tournament, TournamentBracket, Snake, TournamentSnake
from apps.authentication.decorators import admin_required
from datetime import datetime


@admin_required
@login_required
def index(request):
    user = request.user
    return render(request, 'tournament/list.html', {
        'tournaments': Tournament.objects.all(),
        'tournament_brackets': TournamentBracket.objects.all(),
        'user': user,
    })


@admin_required
@login_required
@transaction.atomic
def new(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)

        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.save()
            for snake in form.cleaned_data['snakes']:
                ts = TournamentSnake(tournament=tournament, snake=snake)
                ts.save()
            messages.success(request, f'Tournament "{tournament.name}" successfully created')
            return redirect('/tournaments/')
    else:
        form = TournamentForm(initial={'date': datetime.now()})

    return render(request, 'tournament/new.html', {'form': form})


@admin_required
@login_required
@transaction.atomic
def edit(request, id):
    tournament = Tournament.objects.get(id=id)
    if request.method == 'POST':
        form = TournamentForm(request.POST, instance=tournament)

        if form.is_valid():
            t = form.save(commit=False)
            t.save()
            ts = TournamentSnake.objects.filter(tournament=tournament)

            # Remove snakes from the tournament
            snake_ids = [s.id for s in form.cleaned_data['snakes']]
            for remove in ts.exclude(snake_id__in=snake_ids):
                remove.delete()

            # Add new snakes
            ts_ids = ts.values_list('snake__pk', flat=True)
            for snake in form.cleaned_data['snakes']:
                if snake.id not in ts_ids:
                    ts = TournamentSnake(tournament=tournament, snake=snake)
                    ts.save()

            messages.success(request, f'Tournament group "{tournament.name}" updated')
            return redirect("/tournaments/")
    else:
        form = TournamentForm(instance=tournament)

    return render(request, 'tournament/edit.html', {'form': form})
