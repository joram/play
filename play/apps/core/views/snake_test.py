from apps.authentication.factories import UserFactory
from apps.core.factories import ProfileFactory
from apps.core.models import Snake

user_factory = UserFactory()
profile_factory = ProfileFactory()


def test_create(client):
    user = user_factory.login_as(client)
    profile = profile_factory.profile(user)
    response = client.post(
        "/s/new", {"name": "My Snake", "url": "https://dedsnek.herokuapp.com"}
    )
    assert response.status_code == 301
    snakes = Snake.objects.filter(profile=profile)
    assert snakes.count() == 1
    snake = snakes.first()
    assert snake.name == "My Snake"
    assert snake.url == "https://dedsnek.herokuapp.com"
