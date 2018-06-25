from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.http import urlquote
from django.contrib.auth.decorators import login_required
from apps.game.forms import GameForm


@login_required
def index(request):
    return redirect('/games/new')


@login_required
def new(request):
    return render(request, 'games/new.html', {
        'form': GameForm(),
    })


@login_required
def show(request, id):
    return render(request, 'games/show.html', {
        'id': id,
        'url': f'{settings.BOARD_URL}/?engine={urlquote(settings.ENGINE_URL)}&game={id}'
    })


@login_required
def create(request):
    form = GameForm(request.POST)
    if form.is_valid():
        game_id = form.submit()
        return redirect(f'/games/{game_id}')
    return render(request, 'games/new.html', {
        'form': form,
    })
