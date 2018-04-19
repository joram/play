from apps.play.fields import ShortUUIDField
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser


class User(AbstractBaseUser, PermissionsMixin):
    id = ShortUUIDField(prefix="user", max_length=128, primary_key=True)
    team_id = models.CharField(max_length=128)

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []

    class Meta:
        app_label = 'play'


class Team(models.Model):
    id = ShortUUIDField(prefix="team", max_length=128, primary_key=True)
    team_admin_id = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    description = models.TextField()

    class Meta:
        app_label = 'play'


class Snake(models.Model):
    id = ShortUUIDField(prefix="snake", max_length=128, primary_key=True)
    team_id = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=2084)

    class Meta:
        app_label = 'play'
