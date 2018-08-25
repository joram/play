from django.db import models

from util.fields import ShortUUIDField
from apps.authentication.models import User
from apps.snake.models import Snake


class Team(models.Model):
    id = ShortUUIDField(prefix="tem", max_length=128, primary_key=True)
    name = models.CharField(max_length=128)
    description = models.TextField()
    snake = models.ForeignKey(Snake, on_delete=models.CASCADE)

    class Meta:
        app_label = 'tournament'


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)

    class Meta:
        app_label = 'tournament'
        unique_together = (('team', 'user'))
        ordering = ['id']
