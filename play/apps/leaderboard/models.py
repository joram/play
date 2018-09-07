from django.db import models
from apps.snake.models import UserSnake
from apps.game.models import GameSnake


class UserSnakeLeaderboard(models.Model):
    user_snake = models.ForeignKey(
        UserSnake, primary_key=True, on_delete=models.CASCADE,
    )

    def rank(self):
        return GameSnake.objects.filter(snake_id=self.user_snake_id).aggregate(
            models.Sum('turns'), models.Count(models.Star),
        )

    class Meta:
        app_label = 'leaderboard'
