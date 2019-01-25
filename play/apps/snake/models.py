import os
import requests
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

    def ping(self):
        ping_url = os.path.join(self.url, "/ping")
        response = requests.get(ping_url)
        return response.status_code

    def __str__(self):
        return f'{self.name}'

    class Meta:
        app_label = 'snake'


class UserSnake(BaseModel):
    snake = models.ForeignKey(Snake, on_delete=models.CASCADE, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        app_label = 'snake'
