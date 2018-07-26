from apps.game.models import Game


class GameFactory:
    def basic(self):
        return Game(
            width=10,
            height=10,
            food=5,
        )
