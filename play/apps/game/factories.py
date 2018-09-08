from apps.game.models import Game


class GameFactory:
    def basic(self):
        return Game(
            width=20,
            height=20,
            food=5,
        )
