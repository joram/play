import random
from apps.leaderboard.models import UserSnakeLeaderboard
from apps.game.models import Game
from apps.snake.models import Snake


class MatchStarter:

    def matches(self):
        """ Select matches to run. A random mix of snakes. """
        n = 2
        if UserSnakeLeaderboard.objects.count() > 8:
            n = 4
        snake_ids = list(UserSnakeLeaderboard.objects.all().values_list('user_snake_id', flat=True))
        random.shuffle(snake_ids)
        matches = []
        i = 0
        while i < len(snake_ids):
            matches.append(tuple(snake_ids[i:i + n]))
            i = i + n
        return matches

    def start_game(self, snake_ids):
        """ Start a game given a tuple of snake id's. Returning a game id. """
        snakes = Snake.objects.filter(id__in=snake_ids)
        game = Game(
            width=10,
            height=10,
            food=5,
            snakes=snakes,
        )
        game.save()
        game.run()

    def run(self):
        n = 0
        matches = self.matches()
        for match in matches:
            self.start_game(match)
            n += 1
        return n
