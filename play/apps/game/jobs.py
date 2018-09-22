from apps.game.models import Game


class GameStatusJob:
    """ A job that iterates over all active games and refreshes them. """

    active_statuses = (Game.Status.PENDING, Game.Status.RUNNING, Game.Status.STOPPED)

    def run(self):
        for game in Game.objects.filter(status__in=self.active_statuses):
            try:
                game.update_from_engine()
            except Exception as e:
                # Something wrong with this game, don't care
                print(f'Unable to update game {game.id}')
                pass