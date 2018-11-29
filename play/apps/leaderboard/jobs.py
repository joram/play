import random

from django.db.models import Q

from apps.leaderboard.models import UserSnakeLeaderboard, GameLeaderboard
from apps.game.models import Game
from apps.snake.models import Snake


class MatchStarter:
    def matches(self):
        """ Select matches to run. A random mix of snakes. """
        n = 2
        if UserSnakeLeaderboard.objects.count() > 8:
            n = 4
        snake_ids = list(
            UserSnakeLeaderboard.objects.all().values_list("user_snake_id", flat=True)
        )

        current_leaderboard_games = list(Game.objects.filter(Q(status=Game.Status.RUNNING) | Q(status=Game.Status.PENDING), is_leaderboard_game=True))
        random.shuffle(snake_ids)
        matches = []
        current_match = []

        for snake_id in snake_ids:
            skip = False
            for game in current_leaderboard_games:
                for snake in game.get_snakes():
                    if snake_id == snake.snake.id:
                        skip = True
                        break

            if skip:
                continue

            current_match.append(snake_id)

            if len(current_match) >= n:
                matches.append(current_match)
                current_match = []

        if len(current_match) > 0:
            matches.append(current_match)

        for m in matches:
            if len(m) <= 1:
                matches.remove(m)

        return matches

    def start_game(self, snake_ids):
        """ Start a game given a tuple of snake id's. Returning a game id. """
        if len(snake_ids) == 1:
            return

        snakes = [vars(s) for s in Snake.objects.filter(id__in=snake_ids)]
        game = Game(width=10, height=10, food=5, snakes=snakes)
        game.create()
        game.is_leaderboard_game = True
        game.run()
        GameLeaderboard(game=game).save()

    def run(self):
        n = 0
        matches = self.matches()
        print("matches found", len(matches))
        for match in matches:
            self.start_game(match)
            n += 1
        return n
