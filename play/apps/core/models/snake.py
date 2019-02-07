import os

import requests
from django.db import models

from apps.core.models.profile import Profile
from util.fields import ShortUUIDField
from util.models import BaseModel


class Snake(BaseModel):
    id = ShortUUIDField(prefix="snk", max_length=128, primary_key=True)
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=128)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)

    def ping(self):
        ping_url = os.path.join(self.url, "/ping")
        response = requests.get(ping_url)
        return response.status_code

    def __str__(self):
        return f"{self.name}"
