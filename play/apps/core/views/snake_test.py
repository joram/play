from apps.authentication.factories import UserFactory
from apps.core.factories import ProfileFactory
from apps.core.models import Snake

user_factory = UserFactory()
profile_factory = ProfileFactory()


def test_create(client):
    user = user_factory.login_as(client)
    profile = profile_factory.profile(user)
    response = client.post(
        "/s/new/", {"name": "My Snake", "url": "https://dedsnek.herokuapp.com"}
    )
    assert response.status_code == 302
    snakes = Snake.objects.filter(profile=profile)
    assert snakes.count() == 1

    snake = snakes.first()
    assert f"/u/{user.username}" in response["Location"]
    assert snake.name == "My Snake"
    assert snake.url == "https://dedsnek.herokuapp.com"


def test_get(client):
    user = user_factory.login_as(client)
    profile = profile_factory.profile(user)
    snake = Snake.objects.create(profile=profile, name="My snake")
    response = client.get(f"/s/{snake.id}/")

    assert response.status_code == 200
    assert response.context[-1]["snake"] == snake


def test_edit(client):
    user = user_factory.login_as(client)
    profile = profile_factory.profile(user)
    snake = Snake.objects.create(profile=profile, name="My snake")
    response = client.get(f"/s/{snake.id}/edit/")
    assert response.status_code == 200


def test_update(client):
    user = user_factory.login_as(client)
    profile = profile_factory.profile(user)
    snake = Snake.objects.create(profile=profile, name="My snake")
    response = client.post(
        f"/s/{snake.id}/edit/",
        {"name": "updated-name", "url": "updated-url", "_method": "PUT"},
    )
    assert response.status_code == 302
    snake.refresh_from_db()
    assert snake.name == "updated-name"
    assert snake.url == "updated-url"
