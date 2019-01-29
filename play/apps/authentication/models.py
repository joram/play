from util.fields import ShortUUIDField
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager as DjangoUserManager,
)


class UserManager(DjangoUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        return super()._create_user(username, email, password)


class User(AbstractBaseUser, PermissionsMixin):
    id = ShortUUIDField(prefix="usr", max_length=128, primary_key=True)
    username = models.CharField(
        max_length=39, unique=True
    )  # 39 is max GitHub username length
    email = models.CharField(max_length=512)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        app_label = "authentication"

    @property
    def is_admin(self):
        return self.username.lower() in [
            "brandonb927",
            "bvanvugt",
            "codeallthethingz",
            "coldog",
            "dlsteuer",
            "joram",
            "matthieudolci",
            "tristan-swu",
        ]

    def assigned_to_team(self):
        from apps.tournament.models import TeamMember

        return TeamMember.objects.filter(user_id=self.id).exists()
