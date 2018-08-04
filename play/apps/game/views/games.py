from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.game.forms import GameForm, SnakeForm, get_snakes_from_request
from apps.snake.models import get_user_snakes
from apps.utils.helpers import generate_game_url


@login_required
def index(request):
    return redirect('/games/new')


@login_required
def new(request):
    if request.method == 'POST':
        # GameForm doesn't contain snake data so we have to get it off the request
        game_snakes = get_snakes_from_request(request.POST.dict())
        game_form = GameForm(request.POST, snakes=game_snakes)
        if game_form.is_valid():
            game_id = game_form.submit()
            return redirect(f'/games/{game_id}')
        else:
            status = 400
    else:
        status = 200
        game_form = GameForm()

    snakes = get_user_snakes(request.user)
    SnakeFormSet = formset_factory(
        SnakeForm,
        extra=0,
        min_num=1,
        max_num=10,
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
