import mock

from apps.authentication.factories import UserFactory
from apps.game.factories import GameFactory
from apps.snake.factories import SnakeFactory
from apps.tournament.factories import TeamFactory

user_factory = UserFactory()
team_factory = TeamFactory()
snake_factory = SnakeFactory()
game_factory = GameFactory()


def test_new(client):
    user_factory.login_as(client)
    response = client.get("/games/new/")
    assert response.status_code == 302


def test_new_with_snakes(client):
    user = user_factory.login_as(client)
    snake = snake_factory.basic(n=1, commit=True, user=user)
    team_factory.basic(user=user, snake=snake)
    response = client.get("/games/new/")
    assert response.status_code == 200


@mock.patch("apps.game.engine.run")
def test_show(mock_engine_run, client):
    engine_id = "a879f127-55c2-4b0c-99c9-bce09c9fc0cf"
    url = "game=" + engine_id

    mock_engine_run.return_value = engine_id

    user_factory.login_as(client)
    game = game_factory.basic()
    game.create()
    game.run()

    response = client.get(f"/games/{engine_id}/")
    assert response.status_code == 200
    assert url in response.content.decode("utf-8")
    assert len(mock_engine_run.call_args_list) == 1


@mock.patch("apps.game.engine.run")
def test_create(mock_run, client):
    id = "a879f127-55c2-4b0c-99c9-bce09c9fc0cf"
    mock_run.return_value = id
    user = user_factory.login_as(client)
    snake = snake_factory.basic(n=1, commit=True, user=user)
    team_factory.basic(user=user, snake=snake)

    response = client.post(
        f"/games/new/",
        {
            "width": 10,
            "height": 10,
            "food": 10,
            "board_sizes": "custom",
            # snake formset
            "snake-TOTAL_FORMS": 1,
            "snake-INITIAL_FORMS": 0,
            "snake-MIN_NUM_FORMS": 1,
            "snake-MAX_NUM_FORMS": 8,
            "snake-0-id": snake.id,
            "snake-0-name": snake.name,
            "snake-0-url": snake.url,
        },
    )

    assert response.status_code == 302
    assert len(mock_run.call_args_list) == 1
