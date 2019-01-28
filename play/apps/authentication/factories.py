from apps.authentication.models import User


class UserFactory:
    def basic(self, email="test@test.com", commit=False):
        username = email.split("@")[0]
        user = User(username=username, email=email)
        if commit:
            user.save()
        return user

    def login_as(self, client, email="test@test.com"):
        user = self.basic(email=email, commit=True)
        client.force_login(user, "django.contrib.auth.backends.ModelBackend")
        return user
