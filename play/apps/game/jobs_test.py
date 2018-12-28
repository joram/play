import json

import mock
import uuid
import random
from apps.game.jobs import GameStatusJob
from apps.game.models import Game, GameSnake
from apps.game.factories import GameFactory
from apps.leaderboard.jobs import MatchStarter
from apps.snake.factories import SnakeFactory
from apps.snake.models import UserSnake
from apps.authentication.models import User
from apps.leaderboard.models import UserSnakeLeaderboard, LeaderboardResult

game_factory = GameFactory()
snake_factory = SnakeFactory()


@mock.patch('apps.game.engine.status')
def test_game_status_job(status_mock):
    game = game_factory.basic()
    snakes = snake_factory.basic(n=8, commit=True)

    game.engine_id = str(uuid.uuid4())
    game.snakes = [{'id': snake.id, 'name': snake.name, 'url': snake.url} for snake in snakes]
    game.create()
    game_snakes = GameSnake.objects.filter(game_id=game.id)

    status_mock.return_value = {
        'status': 'running',
        'turn': 10,
        'snakes': {snake.id: {'death': 'starvation'} for snake in game_snakes}
    }

    GameStatusJob().run()

    game = Game.objects.get(id=game.id)
    assert game.status == 'running'
    assert game.turn == 10


@mock.patch('apps.game.engine.status')
@mock.patch('apps.game.engine.run')
def test_update_leaderboard_game(run_mock, status_mock):

    run_mock.return_value = str(uuid.uuid4())

    snakes = snake_factory.basic(n=4, commit=True)
    user_snakes = [UserSnake(snake=s, user=User()) for s in snakes]
    for s in user_snakes:
        s.save()
        UserSnakeLeaderboard.objects.get_or_create(user_snake=s)

    MatchStarter().run()

    game_snakes = GameSnake.objects.all()

    snakes_dict = {snake.id: {'death': 'starvation', 'turn': random.randint(1, 100)} for snake in game_snakes}
    snakes_dict[game_snakes[0].id]['death'] = ''
    snakes_dict[game_snakes[0].id]['turn'] = 125
    snakes_dict[game_snakes[1].id]['turn'] = 125

    status_mock.return_value = {
        'status': Game.Status.COMPLETE,
        'turn': 125,
        'snakes': snakes_dict
    }

    GameStatusJob().run()

    lb = UserSnakeLeaderboard.objects.all()[0]
    assert lb.mu is not None
    assert lb.sigma is not None

    result = LeaderboardResult.objects.get(snake=lb)
    assert result is not None
    assert result.mu_change is not None
    assert result.sigma_change is not None
