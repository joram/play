import trueskill

from apps.game.models import Game, GameSnake
from apps.snake.models import UserSnake
from apps.leaderboard.models import UserSnakeLeaderboard


class GameStatusJob:
    """ A job that iterates over all active games and refreshes them. """

    active_statuses = (Game.Status.PENDING, Game.Status.RUNNING, Game.Status.STOPPED)

    def run(self):
        for game in Game.objects.filter(status__in=self.active_statuses):
            try:
                status = game.update_from_engine()
                if game.is_leaderboard_game and game.status == Game.Status.COMPLETE:
                    sorted_snakes = sorted(sorted(status['snakes'].items(), key=lambda s: s[1]['death']), key=lambda s: s[1]['turn'], reverse=True)
                    game_snake_ids = [s[0] for s in sorted_snakes]
                    game_snakes = GameSnake.objects.filter(id__in=game_snake_ids)
                    snake_ids = [gs.snake_id for gs in game_snakes]
                    snakes = UserSnake.objects.filter(snake_id__in=snake_ids)
                    lb = [UserSnakeLeaderboard.objects.get(user_snake=s) for s in snakes]
                    ratings = [(self.create_rating(l),) for l in lb]
                    new_rankings = trueskill.rate(ratings, ranks=list(range(0, len(ratings))))
                    for x in range(0, len(ratings)):
                        r = new_rankings[x]
                        lb[x].mu = r[0].mu
                        lb[x].sigma = r[0].sigma
                        lb[x].save()

            except Exception as e:
                game.status = Game.Status.ERROR
                game.save()
                # Something wrong with this game, don't care
                print(f'Unable to update game {game.id}', e)
                pass

    def create_rating(self, leaderboard_snake):
        if leaderboard_snake.mu is None or leaderboard_snake.sigma is None:
            return trueskill.Rating()
        return trueskill.Rating(mu=leaderboard_snake.mu, sigma=leaderboard_snake.sigma)