from apps.leaderboard.models import LeaderboardResult


def get_leaderboard_results(snake):
    return (
        LeaderboardResult.objects.filter(snake_id=snake.id)
        .prefetch_related("game")
        .order_by("-modified")[:5]
    )
