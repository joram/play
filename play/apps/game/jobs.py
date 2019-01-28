from collections import OrderedDict

import trueskill

from apps.game.models import Game, GameSnake
from apps.snake.models import UserSnake
from apps.leaderboard.models import UserSnakeLeaderboard, LeaderboardResult


class GameStatusJob:
    """ A job that iterates over all active games and refreshes them. """

    active_statuses = (Game.Status.PENDING, Game.Status.RUNNING, Game.Status.STOPPED)

    def run(self):
        for game in Game.objects.filter(status__in=self.active_statuses):
            try:
                status = game.update_from_engine()
                if game.leaderboard_game and game.status == Game.Status.COMPLETE:
                    sorted_snakes = sorted(
                        sorted(status["snakes"].items(), key=lambda s: s[1]["death"]),
                        key=lambda s: s[1]["turn"],
                        reverse=True,
                    )
                    snake_lookup = OrderedDict()
                    for s in sorted_snakes:
                        snake_lookup[s[0]] = {}
                    game_snakes = GameSnake.objects.filter(
                        id__in=list(snake_lookup.keys())
                    )
                    for gs in game_snakes:
                        snake_lookup[gs.id]["snake_id"] = gs.snake_id
                    snake_ids = [snake_lookup[s]["snake_id"] for s in snake_lookup]
                    for us in UserSnake.objects.filter(snake_id__in=snake_ids):
                        for gs_id, data in snake_lookup.items():
                            if data["snake_id"] == us.snake.id:
                                snake_lookup[gs_id]["user_snake"] = us
                    snakes = [snake_lookup[i]["user_snake"] for i in snake_lookup]
                    lb = [
                        UserSnakeLeaderboard.objects.get(user_snake=s) for s in snakes
                    ]
                    for l in lb:
                        for gs_id, data in snake_lookup.items():
                            if data["user_snake"].snake.id == l.user_snake.snake.id:
                                data["rating"] = (self.create_rating(l),)
                                data["leaderboard"] = l
                    ratings = [snake_lookup[i]["rating"] for i in snake_lookup]
                    new_rankings = trueskill.rate(
                        ratings, ranks=list(range(0, len(ratings)))
                    )
                    items = list(snake_lookup.items())
                    for x in range(0, len(ratings)):
                        r = new_rankings[x]
                        current = items[x][1]["leaderboard"]
                        current.mu = r[0].mu
                        current.sigma = r[0].sigma
                        current.save()
                        result = LeaderboardResult(
                            snake=current,
                            game=game,
                            mu_change=current.mu - ratings[x][0].mu,
                            sigma_change=current.sigma - ratings[x][0].sigma,
                        )
                        result.save()

            except Exception as e:
                game.status = Game.Status.ERROR
                game.save()
                # Something wrong with this game, don't care
                print(f"Unable to update game {game.id}", e)
                pass

    def create_rating(self, leaderboard_snake):
        if leaderboard_snake.mu is None or leaderboard_snake.sigma is None:
            return trueskill.Rating()
        return trueskill.Rating(mu=leaderboard_snake.mu, sigma=leaderboard_snake.sigma)
