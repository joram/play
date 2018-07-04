from util.fields import ShortUUIDField
from django.db import models
from django.contrib.auth.models import (
    PermissionsMixin, AbstractBaseUser, UserManager as DjangoUserManager
)


class UserManager(DjangoUserManager):

    def _create_user(self, username, email, password, **extra_fields):
        if 'is_staff' in extra_fields:
            del extra_fields['is_staff']
        return DjangoUserManager._create_user(
            self, username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = ShortUUIDField(prefix="usr", max_length=128, primary_key=True)
    team_id = models.CharField(max_length=128)
    username = models.CharField(max_length=39, unique=True)
    email = models.CharField(max_length=512)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        app_label = 'authentication'
