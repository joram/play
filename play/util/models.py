from django.db import models

from util.fields import CreatedDateTimeField, ModifiedDateTimeField


class BaseModel(models.Model):
    created = CreatedDateTimeField()
    modified = ModifiedDateTimeField()

    class Meta:
        abstract = True
