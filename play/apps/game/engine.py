import requests
from django.conf import settings


def run_game(config):
    res = requests.post(f'{settings.ENGINE_URL}/games', json=config)
    res.raise_for_status()
    game_id = res.json()['ID']

    res = requests.post(f'{settings.ENGINE_URL}/games/{game_id}/start')
    res.raise_for_status()
    return game_id
