from django.conf import settings
from django.utils.http import urlquote


def generate_game_url(game_id):
    return (
        f"{settings.BOARD_URL}/?engine={urlquote(settings.ENGINE_URL)}&game={game_id}"
    )
