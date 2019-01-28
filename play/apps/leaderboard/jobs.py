import random

from django.db.models import Q

from apps.leaderboard.models import UserSnakeLeaderboard, GameLeaderboard
from apps.game.models import Game
from apps.snake.models import Snake


class MatchStarter:
    def chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i : i + n]

    def matches(self):
        """ Select matches to run. A random mix of snakes. """
        snake_ids = list(
            UserSnakeLeaderboard.objects.all().values_list("user_snake_id", flat=True)
        )

        current_leaderboard_games = list(
            GameLeaderboard.objects.filter(
                Q(game__status=Game.Status.RUNNING)
                | Q(game__status=Game.Status.PENDING)
            )
        )
        for lb_game in current_leaderboard_games:
            for gs in lb_game.game.get_snakes():
                if gs.snake.id in snake_ids:
                    snake_ids.remove(gs.snake.id)
        random.shuffle(snake_ids)
        match_size = random.randint(0, 3) + 5
        print("Creating matches of size:", match_size)
        return [m for m in list(self.chunks(snake_ids, match_size)) if len(m) > 1]

    def start_game(self, snake_ids):
        """ Start a game given a tuple of snake id's. Returning a game id. """
        if len(snake_ids) == 1:
            return

        snakes = [vars(s) for s in Snake.objects.filter(id__in=snake_ids)]
        game = Game(width=10, height=10, food=5, snakes=snakes)
        game.create()
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
