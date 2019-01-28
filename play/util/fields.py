import shortuuid
from django.db import models
from django.db.models import DateTimeField

from util.time import now as time_now


class CreatedDateTimeField(DateTimeField):
    """
    CreationDateTimeField
    By default, sets editable=False, blank=True, default=now
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("editable", False)
        kwargs.setdefault("blank", True)
        kwargs.setdefault("default", time_now)
        DateTimeField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "DateTimeField"

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector

        field_class = "django.db.models.fields.DateTimeField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class ModifiedDateTimeField(CreatedDateTimeField):
    """
    ModificationDateTimeField
    By default, sets editable=False, blank=True, default=now
    Sets value to now on each save of the model.
    """

    def pre_save(self, model, add):
        value = time_now()
        setattr(model, self.attname, value)
        return value

    def get_internal_type(self):
        return "DateTimeField"

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector

        field_class = "django.db.models.fields.DateTimeField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class ShortUUIDField(models.CharField):
    ALPHABET = "346789BCDFGHJKMPQRSTVWXYbcdfghjkmpqrtvwxy"  # 41 chars total

    def __init__(self, prefix=None, *args, **kwargs):
        super(ShortUUIDField, self).__init__(*args, **kwargs)
        self.__prefix = prefix

    def create_uuid(self):
        short_uuid = shortuuid.ShortUUID()
        short_uuid.set_alphabet(ShortUUIDField.ALPHABET)

        uuid = short_uuid.uuid()

        if self.__prefix:
            uuid = "{}_{}".format(self.__prefix, uuid)

        uuid = uuid[: self.max_length]

        return uuid

    def get_default(self):
        uuid = self.create_uuid()
        return uuid

    def to_python(self, value):
        return value
