from django.db import models
from util.fields import ShortUUIDField
from util.models import BaseModel
from apps.authentication.models import User


def get_user_snakes(user):
    return [
        user_snake.snake
        for user_snake in UserSnake.objects.filter(user_id=user.id).prefetch_related('snake')
    ]


class Snake(BaseModel):
    id = ShortUUIDField(prefix="snk", max_length=128, primary_key=True)
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        app_label = 'snake'

    def get_leaderboard_games(self):
        from apps.game.models import Game
        return Game.objects.filter(gamesnake__snake_id=self.id, is_leaderboard_game=True).order_by("-modified")[:5]


class UserSnake(BaseModel):
    snake = models.ForeignKey(Snake, on_delete=models.CASCADE, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        app_label = 'snake'
