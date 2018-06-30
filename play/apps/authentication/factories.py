from apps.authentication.models import User


class UserFactory:
    def login_as(self, client, email='test@test.com'):
        username = email.split('@')[0]
        user = User(username=username, email=email)
        user.save()
        client.force_login(user, 'django.contrib.auth.backends.ModelBackend')
