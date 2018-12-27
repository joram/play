from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from apps.game.models import Game
from apps.game.forms import GameForm, SnakeForm, get_snakes_from_request
from apps.snake.models import UserSnake, get_user_snakes
from apps.tournament.middleware import with_current_team
from apps.utils.helpers import generate_game_url


@login_required
@with_current_team
def index(request):
    games = Game.objects.filter(
        team_id=request.team.id
    ).order_by('-status', 'created')

    if games.count() == 0:
        return redirect('/games/new')

    for game in games:
        game.snakes = game.get_snakes()

    return render(request, 'games/list.html', {
        'games': games,
    })


@login_required
@with_current_team
def new(request):
    if request.method == 'POST':
        # GameForm doesn't contain snake data so we have to get it off the request
        game_snakes = get_snakes_from_request(request.POST.dict())
        game_form = GameForm(request.POST, snakes=game_snakes, team=request.team)
        if game_form.is_valid():
            game_id = game_form.submit()
            return redirect(f'/games/{game_id}')
        else:
            status = 400
    else:
        # Users with no snakes need to create one first
        snakes = get_user_snakes(request.user)
        if len(snakes) == 0:
            messages.warning(request, 'You must add at least one snake to start a game!')
            return redirect('/snakes/new/')

        status = 200
        game_form = GameForm()

    snakes = get_user_snakes(request.user)
    SnakeFormSet = formset_factory(
        SnakeForm,
        extra=0,
        min_num=8,
        max_num=8,
        validate_min=True,
        validate_max=True,
    )
    snake_formset = SnakeFormSet(prefix='snake')

    return render(request, 'games/new.html', {
        'game_form': game_form,
        'snake_formset': snake_formset,
        'snakes': snakes,
    }, status=status)


@login_required
def show(request, id):
    return render(request, 'games/show.html', {
        'id': id,
        'url': generate_game_url(id)
    })
