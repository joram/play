from apps.platform.models import Player


class PlayerFactory:
    def player(self, user):
        return Player.objects.create(user=user)
