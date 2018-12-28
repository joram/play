from django.db import models

from apps.game.models import Game
from apps.snake.models import UserSnake
from util.models import BaseModel


class GameLeaderboard(BaseModel):
    """ Tracks a game from the leaderboard perspective. """

    game = models.OneToOneField(Game, null=True, blank=True, on_delete=models.SET_NULL)


class UserSnakeLeaderboard(BaseModel):
    """ Tracks a snakes involvement in the leaderboard. """

    def __init__(self, *args, **kwargs):
        self._rank = False
        super().__init__(*args, **kwargs)

    user_snake = models.ForeignKey(
        UserSnake, primary_key=True, on_delete=models.CASCADE
    )
    mu = models.FloatField(null=True)
    sigma = models.FloatField(null=True)

    @classmethod
    def ranked(cls):
        snakes = list(UserSnakeLeaderboard.objects.all())
        return sorted(snakes, key=lambda s: s.mu or 25)

    def __str__(self):
        return f'{self.user_snake.snake.name}'

    class Meta:
        app_label = 'leaderboard'


class LeaderboardResult(BaseModel):
    snake = models.ForeignKey(UserSnakeLeaderboard, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    mu_change = models.FloatField()
    sigma_change = models.FloatField()
