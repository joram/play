from apps.game.models import Game


class GameStatusJob:
    """ A job that iterates over all active gamees and refreshes them. """

    filters = dict(
        # status__in=(Game.Status.PENDING, Game.Status.RUNNING, Game.Status.STOPPED)
    )

    def run(self):
        for game in Game.objects.filter(**self.filters):
            game.update_from_engine()
