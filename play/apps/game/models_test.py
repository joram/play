import mock
import uuid

from apps.game.models import GameSnake
from apps.snake.factories import SnakeFactory
from apps.game.factories import GameFactory

snake_factory = SnakeFactory()
game_factory = GameFactory()


def test_game_engine_configuration():
    game = game_factory.basic()
    snakes = snake_factory.basic(n=8, commit=True)
    game.snakes = [{'id': snake.id, 'name': snake.name, 'url': snake.url} for snake in snakes]
    game.create()

    config = game.config()
    assert config['height'] == 20
    assert config['width'] == 20
    assert config['food'] == 5
    assert config['snakes'][0]['id'] is not None
    assert config['snakes'][0]['name'] == 'test'
    assert len(config['snakes']) == 8


@mock.patch('apps.game.engine.run')
def test_game_engine_call(run_mock):
    run_mock.return_value = str(uuid.uuid4())

    game = game_factory.basic()
    snakes = snake_factory.basic(n=8, commit=True)
    game.snakes = [{'id': snake.id, 'name': snake.name, 'url': snake.url} for snake in snakes]
    game.create()
    assert game.engine_id is None

    game.run()
    assert len(run_mock.call_args_list) == 1
    assert game.engine_id is not None


@mock.patch('apps.game.engine.status')
def test_game_engine_update(status_mock):
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

    game.update_from_engine()
    assert len(status_mock.call_args_list) == 1
    assert game.status == 'running'
    assert game.turn == 10
