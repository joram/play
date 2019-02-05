from apps.core.models import Profile


class ProfileFactory:
    def profile(self, user):
        return Profile.objects.create(user=user)
