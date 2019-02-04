from apps.platform.factories import PlayerFactory
from apps.authentication.factories import UserFactory

user_factory = UserFactory()
player_factory = PlayerFactory()


def test_get(client):
    user = user_factory.login_as(client)
    player = player_factory.player(user)
    response = client.get(f"/players/{player.username}/")
    assert response.status_code == 200
