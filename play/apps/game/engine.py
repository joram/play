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

    status = data['Game'].get('Status', 'pending')
    turn = data['LastFrame'].get('Turn', 0)
    gsnakes = data['LastFrame'].get('Snakes', [])

    snakes = {}
    for s in gsnakes:
        id = s['ID']
        snakes[id] = {
            'death': s['Death']['Cause'] if s['Death'] else ''
            'turn': s['Death']['Turn'] if s['Death'] else turn
        }

    return {
        'status': status,
        'turn': turn,
        'snakes': snakes,
    }
    return {'status': status, 'turn': turn, 'snakes': snakes}
