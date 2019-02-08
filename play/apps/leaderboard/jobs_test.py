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
@mock.patch("apps.game.engine.create")
@mock.patch("random.randint")
def test_game_status_job(rand_mock, create_mock, run_mock):
    rand_mock.return_value = 0
    user = user_factory.basic()
    create_mock.return_value = lambda: uuid.uuid4()
    snakes = snake_factory.basic(n=6, commit=True)
    for s in snakes:
        user_snake = UserSnake.objects.create(snake=s, user=user)
        UserSnakeLeaderboard.objects.create(user_snake=user_snake)

    existing_game_snakes = [snake.id for snake in snakes[0:2]]
    MatchStarter().start_game(existing_game_snakes)
    # reset this run game call, because it's setup.
    create_mock.reset_mock()
    run_mock.reset_mock()

    count = MatchStarter().run()
    assert count == 1
    assert len(create_mock.call_args_list) == 1
    assert len(create_mock.call_args_list[0][0][0]["snakes"]) == 4
