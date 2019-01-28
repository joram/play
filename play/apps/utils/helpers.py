from django.conf import settings
from django.utils.http import urlquote


def generate_game_url(id):
    return f"{settings.BOARD_URL}/?engine={urlquote(settings.ENGINE_URL)}&game={id}"
