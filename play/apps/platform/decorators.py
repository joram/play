from apps.platform.models import Player


def with_player(action):
    def wrapper(request, *args, **kwargs):
        try:
            player = Player.objects.get(user=request.user)
        except Player.DoesNotExist:
            player = Player(user=request.user)
        request.player = player
        return action(request, *args, **kwargs)

    return wrapper
