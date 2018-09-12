from django.db import models
from util.fields import ShortUUIDField
from apps.authentication.models import User


def get_user_snakes(user):
    return [
        user_snake.snake
        for user_snake in UserSnake.objects.filter(user_id=user.id).prefetch_related('snake')
    ]


class Snake(models.Model):
    id = ShortUUIDField(prefix="snk", max_length=128, primary_key=True)
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=128)

    class Meta:
        app_label = 'snake'


class UserSnake(models.Model):
    snake = models.ForeignKey(Snake, on_delete=models.CASCADE, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        app_label = 'snake'
