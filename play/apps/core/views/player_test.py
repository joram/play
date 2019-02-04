from apps.core.models import Profile
from apps.core.factories import ProfileFactory
from apps.authentication.factories import UserFactory

user_factory = UserFactory()
profile_factory = ProfileFactory()


def test_edit(client):
    user_factory.login_as(client)
    response = client.get("/profile/")
    assert response.status_code == 200


def test_update(client):
    user = user_factory.login_as(client)
    response = client.post("/profile/", {"email": "my-new-email", "_method": "PUT"})
    assert response.status_code == 302
    assert Profile.objects.get(user=user).email == "my-new-email"


def test_update_no_email(client):
    user_factory.login_as(client)
    response = client.post("/profile/", {"email": "", "_method": "PUT"})
    assert response.status_code == 400


def test_delete(client):
    user = user_factory.login_as(client)
    profile_factory.profile(user)
    response = client.delete("/profile/")
    assert response.status_code == 302
