from django.db import models

from apps.authentication.models import User
from util.models import BaseModel


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # Has opted in to marketing emails and communications.
    optin_marketing = models.BooleanField(default=False, null=False)

    @property
    def email(self):
        return self.user.email

    @property
    def username(self):
        return self.user.username

    @property
    def snakes(self):
        return self.snake_set.all()
