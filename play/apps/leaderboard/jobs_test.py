import mock
import uuid
from apps.leaderboard.models import UserSnakeLeaderboard
from apps.leaderboard.jobs import MatchStarter
from apps.authentication.factories import UserFactory
from apps.snake.factories import SnakeFactory
from apps.snake.models import UserSnake


user_factory = UserFactory()
snake_factory = SnakeFactory()


@mock.patch("apps.game.engine.run")
def test_game_status_job(run_mock):
    user = user_factory.basic()
    run_mock.return_value = lambda: uuid.uuid4()
    snakes = snake_factory.basic(n=10, commit=True)
    for s in snakes:
        user_snake = UserSnake.objects.create(snake=s, user=user)
        UserSnakeLeaderboard.objects.create(user_snake=user_snake)

    count = MatchStarter().run()
    assert count == 3
    assert len(run_mock.call_args_list) == 3
