from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.leaderboard.models import UserSnakeLeaderboard


@login_required
def index(request):
    ranked = sorted([{
        'name': snake.user_snake.snake.name,
        'rank': snake.mu or 25,
        'games': snake.user_snake.snake.get_leaderboard_games()
    } for snake in UserSnakeLeaderboard.ranked()], key=lambda s: s['rank'], reverse=True)
    return render(
        request, 'leaderboard/index.html', {
            'ranked': ranked,
            'user': request.user,
            'user': request.user,
        }
    )
