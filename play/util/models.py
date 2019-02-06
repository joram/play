from django.db import models

from util.fields import CreatedDateTimeField, ModifiedDateTimeField


class BaseManager(models.Manager):
    def get_or_init(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return self.model(**kwargs)


class BaseModel(models.Model):
    created = CreatedDateTimeField()
    modified = ModifiedDateTimeField()

    objects = BaseManager()

    class Meta:
        abstract = True

    def is_saved(self):
        return not self._state.adding
