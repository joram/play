from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.tournament.forms import TournamentSnakeForm
from apps.tournament.models import TournamentBracket, TournamentSnake
from apps.authentication.decorators import admin_required


@admin_required
@login_required
@transaction.atomic
def new(request, id):
    tournament_bracket = TournamentBracket.objects.get(id=id)
    if request.method == 'POST':
        form = TournamentSnakeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully added "{form.cleaned_data["snake"].name}" to tournament bracket "{form.cleaned_data["bracket"].name}"')
            return redirect('/tournaments/')
    else:
        form = TournamentSnakeForm()
        form.bracket = tournament_bracket

    return render(request, 'tournament_bracket_snake/new.html', {
        'form': form,
        'tournament_bracket': tournament_bracket,
    })
