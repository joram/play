import shortuuid
from django.db import models


class ShortUUIDField(models.CharField):
    ALPHABET = '346789BCDFGHJKMPQRSTVWXYbcdfghjkmpqrtvwxy'  # 41 chars total

    def __init__(self, prefix=None, *args, **kwargs):
        super(ShortUUIDField, self).__init__(*args, **kwargs)
        self.__prefix = prefix

    def create_uuid(self):
        short_uuid = shortuuid.ShortUUID()
        short_uuid.set_alphabet(ShortUUIDField.ALPHABET)

        uuid = short_uuid.uuid()

        if self.__prefix:
            uuid = '{}_{}'.format(self.__prefix, uuid)

        uuid = uuid[:self.max_length]

        return uuid

    def get_default(self):
        uuid = self.create_uuid()
        return uuid

    def to_python(self, value):
        return value