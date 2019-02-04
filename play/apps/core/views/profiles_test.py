from apps.core.factories import ProfileFactory
from apps.authentication.factories import UserFactory

user_factory = UserFactory()
profile_factory = ProfileFactory()


def test_get(client):
    user = user_factory.login_as(client)
    profile = profile_factory.profile(user)
    response = client.get(f"/u/{profile.username}/")
    assert response.status_code == 200
