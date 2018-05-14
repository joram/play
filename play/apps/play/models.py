from apps.play.fields import ShortUUIDField
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, UserManager as DjangoUserManager


class UserManager(DjangoUserManager):

    def _create_user(self, username, email, password, **extra_fields):
        if 'is_staff' in extra_fields:
            del extra_fields['is_staff']
        return DjangoUserManager._create_user(self, username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = ShortUUIDField(prefix="user", max_length=128, primary_key=True)
    team_id = models.CharField(max_length=128)
    username = models.CharField(max_length=39, unique=True)
    email = models.CharField(max_length=512)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

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
