from apps.core.factories import ProfileFactory
from apps.authentication.factories import UserFactory
from apps.core.models import Snake

user_factory = UserFactory()
profile_factory = ProfileFactory()


def test_get(client):
    user = user_factory.login_as(client)
    profile = profile_factory.profile(user)
    response = client.get(f"/u/{profile.username}/")
    assert response.status_code == 200


def test_snakes_are_returned_in_response(client):
    user = user_factory.login_as(client)
    profile = profile_factory.profile(user)
    Snake.objects.create(profile=profile, name="My Snake")
    response = client.get(f"/u/{profile.username}/")

    assert response.context[-1]["profile"].snakes[0].name == "My Snake"
