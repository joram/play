import mock
import uuid
from apps.game.jobs import GameStatusJob
from apps.game.models import Game, GameSnake
from apps.game.factories import GameFactory
from apps.snake.factories import SnakeFactory


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
