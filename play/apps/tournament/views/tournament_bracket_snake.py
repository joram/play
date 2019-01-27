from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.tournament.models import TournamentBracket, Heat, Snake
from apps.authentication.decorators import admin_required


@admin_required
@login_required
@transaction.atomic
def new(request, id):
    tournament_bracket = TournamentBracket.objects.get(id=id)
    if request.method == 'POST':
        form = SnakeTournamentBracketForm(request.POST)

        if form.is_valid():
            form.save()
            snake_id = form.data['snake']
            bracket_id = form.data['tournament_bracket']
            snake = Snake.objects.get(id=snake_id)
            bracket = TournamentBracket.objects.get(id=bracket_id)
            messages.success(request, f'Successfully added "{snake.name}" to tournament bracket "{bracket}"')
            return redirect('/tournaments/')
    else:
        form = SnakeTournamentBracketForm()
        form.tournament_bracket = tournament_bracket

    # TODO Left by @tristan-swu: Need to review this with John
    return render(request, 'tournament_bracket_snake/new.html', {
        # 'form': form,
        'tournament_bracket': tournament_bracket,
    })
