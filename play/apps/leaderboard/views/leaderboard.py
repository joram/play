from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.leaderboard.models import UserSnakeLeaderboard


@login_required
def index(request):
    ranked = [
        {'name': snake.user_snake.snake.name, 'rank': snake.rank()}
        for snake in UserSnakeLeaderboard.ranked()
    ]
    return render(
        request, 'leaderboard/index.html', {'ranked': ranked, 'user': request.user}
    )
