from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.snake.models import UserSnake
from apps.leaderboard.models import UserSnakeLeaderboard


@login_required
def index(request):
    snakes = [
        {
            'id': user_snake.snake.id,
            'name': user_snake.snake.name,
            'registered': UserSnakeLeaderboard.objects.filter(user_snake=user_snake).first() is not None,
        } for user_snake in
        UserSnake.objects.filter(user_id=request.user.id).
        prefetch_related('snake')
    ]
    return render(request, 'leaderboard/snakes.html', {
        'snakes': snakes,
        'user': request.user,
    })


@login_required
@transaction.atomic
def create(request, id):
    user_snake = UserSnake.objects.get(snake_id=id, user_id=request.user.id)
    UserSnakeLeaderboard.objects.get_or_create(user_snake=user_snake)
    return redirect('/leaderboard/snakes')


@login_required
@transaction.atomic
def delete(request, id):
    user_snake = UserSnake.objects.get(snake_id=id, user_id=request.user.id)
    try:
        UserSnakeLeaderboard.objects.get(user_snake=user_snake).delete()
    except UserSnakeLeaderboard.DoesNotExist:
        pass
    return redirect('/leaderboard/snakes')
