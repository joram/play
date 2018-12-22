from settings.base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": get_env("POSTGRES_DB", "battlesnakeio_play", True),
        "USER": get_env("POSTGRES_USER", None, False),
        "PASSWORD": get_env("POSTGRES_PASSWORD", None, False),
        "HOST": get_env("POSTGRES_HOST", None, False),
        "PORT": get_env("POSTGRES_PORT", None, False),
    }}

