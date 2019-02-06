from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.core.forms import SnakeForm
from apps.core.middleware import profile_required
from apps.core.models import Snake


def show(request, snake_id):
    snake = Snake.objects.get(id=snake_id)
    return render(request, "snake/show.html", {"snake": snake})


@login_required
@profile_required
def new(request):
    form = SnakeForm()
    return render(request, "snake/new.html", {"form": form})


@login_required
@profile_required
def create(request):
    form = SnakeForm(request.POST)
    if form.is_valid():
        snake = form.save(commit=False)
        snake.profile = request.user.profile
        snake.save()
        return redirect(f"/u/{request.user.username}")
    return render(request, "snake/edit.html", {"form": form})


@login_required
@profile_required
def edit(request, snake_id):
    try:
        snake = Snake.objects.get(id=snake_id, profile=request.user.profile)
        form = SnakeForm(instance=snake)
        return render(request, "snake/edit.html", {"form": form})
    except Snake.DoesNotExist:
        return redirect(f"/s/{snake_id}")


@login_required
@profile_required
def update(request, snake_id):
    snake = Snake.objects.get(id=snake_id, profile=request.user.profile)
    form = SnakeForm(request.POST, instance=snake)
    if form.is_valid():
        snake = form.save(commit=False)
        snake.profile = request.user.profile
        snake.save()
        return redirect(f"/u/{request.user.username}")
    return render(request, "snake/edit.html", {"form": form})
