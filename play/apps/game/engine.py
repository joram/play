import requests
from django.conf import settings


def run(config):
    res = requests.post(f'{settings.ENGINE_URL}/games', json=config)
    res.raise_for_status()
    game_id = res.json()['ID']

    res = requests.post(f'{settings.ENGINE_URL}/games/{game_id}/start')
    res.raise_for_status()
    return game_id


def status(id):
    res = requests.get(f'{settings.ENGINE_URL}/games/{id}')
    res.raise_for_status()
    data = res.json()

    status = data['Game']['Status']
    turn = data['LastFrame']['Turn']
    snakes = {
        s['ID']: {'death': s['Death']} for s in data['LastFrame']['Snakes']
    }
    return {
        'status': status,
        'turn': turn,
        'snakes': snakes,
    }
