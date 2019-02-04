from apps.core.models import Profile


def with_profile(action):
    """
    With profile is simple middleware that ensures that a profile is
    instantiated on the user object.
    """

    def middleware(request, *args, **kwargs):
        if not hasattr(request.user, "profile"):
            request.user.profile = Profile(user=request.user)
        return action(request)

    return middleware
