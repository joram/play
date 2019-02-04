from django.db import models
from apps.authentication.models import User
from util.models import BaseModel


class Player(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    @property
    def email(self):
        return self.user.email

    @property
    def username(self):
        return self.user.username
