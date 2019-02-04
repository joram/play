from apps.platform.models import Player
from apps.platform.factories import PlayerFactory
from apps.authentication.factories import UserFactory

user_factory = UserFactory()
player_factory = PlayerFactory()


def test_edit(client):
    user_factory.login_as(client)
    response = client.get("/profile")
    assert response.status_code == 200


def test_update(client):
    user = user_factory.login_as(client)
    response = client.post("/profile", {"email": "my-new-email", "_method": "PUT"})
    assert response.status_code == 302
    assert Player.objects.get(user=user).email == "my-new-email"


def test_delete(client):
    user = user_factory.login_as(client)
    player_factory.player(user)
    response = client.delete("/profile")
    assert response.status_code == 302
