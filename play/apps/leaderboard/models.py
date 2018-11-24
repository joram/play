from django.db import models, connection
from apps.snake.models import UserSnake
from apps.game.models import Game


class GameLeaderboard(models.Model):
    """ Tracks a game from the leaderboard perspective. """

    game = models.ForeignKey(Game, primary_key=True, on_delete=models.CASCADE)


class UserSnakeLeaderboard(models.Model):
    """ Tracks a snakes involvement in the leaderboard. """

    def __init__(self, *args, **kwargs):
        self._rank = False
        super().__init__(*args, **kwargs)

    user_snake = models.ForeignKey(
        UserSnake, primary_key=True, on_delete=models.CASCADE
    )
    mu = models.FloatField(null=True)
    sigma = models.FloatField(null=True)

    @classmethod
    def ranked(cls):
        snakes = list(UserSnakeLeaderboard.objects.all())
        return sorted(snakes, key=lambda s: s.mu or 25)

    def rank(self):
        """
        Given the snake ID for the leaderboard. Aggregate all of the turns this
        snake has taken throughout the leaderboard.
        """
        if self._rank is not False:
            return self._rank
        with connection.cursor() as cursor:
            cursor.execute(
                """
SELECT SUM(game_gamesnake.turns) FROM game_gamesnake
JOIN game_game on game_gamesnake.game_id = game_game.id
JOIN leaderboard_gameleaderboard on leaderboard_gameleaderboard.game_id = game_game.id
WHERE game_gamesnake.snake_id = %s
            """,
                [self.user_snake_id],
            )
            row = cursor.fetchone()
        self._rank = row[0] or 0
        return self._rank

    class Meta:
        app_label = 'leaderboard'
