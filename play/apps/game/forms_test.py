import mock
import uuid
from apps.game.forms import GameForm
from apps.snake.factories import SnakeFactory


snake_factory = SnakeFactory()


@mock.patch("apps.game.engine.run")
def test_submit(mock_run):
    engine_id = str(uuid.uuid4())
    mock_run.return_value = engine_id

    snake = snake_factory.basic(n=1, commit=True)

    form = GameForm(
        {"width": 10, "height": 10, "food": 10, "board_sizes": "custom"},
        snakes=[{"id": snake.id, "name": snake.name, "url": snake.url}],
    )

    assert form.is_valid()
    assert form.submit() == engine_id
    assert len(mock_run.call_args_list) == 1
