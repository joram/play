from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.snake.models import UserSnake
from apps.snake.forms import SnakeForm


@login_required
def index(request):
    snakes = [
        user_snake.snake for user_snake in
        UserSnake.objects.filter(user_id=request.user.id).
        prefetch_related('snake')
    ]
    return render(request, 'snakes/index.html', {
        'snakes': snakes,
        'user': request.user,
    })


@login_required
def new(request):
    return render(request, 'snakes/new.html', {
        'form': SnakeForm(request.user),
    })


@login_required
def edit(request, id):
    snake = UserSnake.objects.get(snake_id=id, user_id=request.user.id).snake
    return render(request, 'snakes/edit.html', {
        'form': SnakeForm(request.user, instance=snake),
        'user': request.user,
        'snake': snake,
    })


@login_required
@transaction.atomic
def create(request):
    form = SnakeForm(request.user, request.POST)
    if form.is_valid():
        form.save()
        return redirect('/snakes')
    return render(request, 'snakes/new.html', {
        'form': form,
    }, status=400)


@login_required
@transaction.atomic
def update(request, id):
    snake = UserSnake.objects.get(snake_id=id, user_id=request.user.id).snake
    form = SnakeForm(request.user, request.POST, instance=snake)
    if form.is_valid():
        form.save()
        return redirect('/snakes')
    return render(request, 'snakes/edit.html', {
        'form': form,
    }, status=400)


@login_required
@transaction.atomic
def delete(request, id):
    snake = UserSnake.objects.get(snake_id=id, user_id=request.user.id).snake
    snake.delete()
    return redirect('/snakes')
