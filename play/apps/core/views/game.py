from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from apps.core.forms import GameForm
from apps.core.middleware import profile_required
from apps.core.models import Snake, Game
from apps.utils.helpers import generate_game_url


@login_required
def new(request):
    snake_ids = request.GET.get("snake-ids")
    form = GameForm(initial={"snakes": snake_ids})
    return render(request, "game/new.html", {"form": form})


@login_required
@profile_required
def create(request):
    form = GameForm(request.POST)
    if form.is_valid():
        game = form.save(request.user.profile)
        game.create()
        game.run()
        return redirect(f"/g/{game.id}")
    return render(request, "game/new.html", {"form": form})


@login_required
@profile_required
def snake_autocomplete(request):
    s = Snake.objects.filter(
        Q(is_public=True) | Q(profile=request.user.profile)
    ).prefetch_related("profile__user")
    q = request.GET.get("q")
    if len(q) == 0:
        s = Snake.objects.none()

    return JsonResponse(
        [
            {"value": snake.id, "text": f"{snake.profile.username}/{snake.name}"}
            for snake in s
            if q in snake.profile.username or q in snake.name
        ],
        safe=False,
    )


@login_required
@profile_required
def snake_info(request):
    snake_ids = request.GET.get("snakes", "").split(",")
    s = Snake.objects.filter(
        Q(id__in=snake_ids) & (Q(is_public=True) | Q(profile=request.user.profile))
    )
    return JsonResponse(
        [
            {"value": snake.id, "text": f"{snake.profile.username}/{snake.name}"}
            for snake in s
        ],
        safe=False,
    )


def show(request, game_id):
    game = Game.objects.get(id=game_id)
    return render(request, "game/show.html", {"url": generate_game_url(game.engine_id)})
