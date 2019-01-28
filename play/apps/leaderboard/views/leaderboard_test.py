from apps.authentication.factories import UserFactory

user_factory = UserFactory()


def test_index(client):
    user_factory.login_as(client)
    response = client.get("/leaderboard/")
    assert response.status_code == 200
