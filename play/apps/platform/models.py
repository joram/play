from django.db import models
from apps.authentication.models import User
from util.models import BaseModel
from util.fields import ShortUUIDField


class Player(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    @property
    def snakes(self):
        return Snake.objects.filter(player=self)

    @property
    def email(self):
        return self.user.email

    @property
    def username(self):
        return self.user.username


class Snake(BaseModel):
    id = ShortUUIDField(prefix="snk", max_length=128, primary_key=True)
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=128)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
