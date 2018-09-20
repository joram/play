from apps.game.models import Game


class GameStatusJob:
<<<<<<< Updated upstream
    """ A job that iterates over all active games and refreshes them. """
    active_statuses = (
        Game.Status.PENDING,
        Game.Status.RUNNING,
        Game.Status.STOPPED,
=======
    """ A job that iterates over all active gamees and refreshes them. """

    filters = dict(
        status__in=(Game.Status.PENDING, Game.Status.RUNNING, Game.Status.STOPPED)
>>>>>>> Stashed changes
    )

    def run(self):
        for game in Game.objects.filter(**self.filters):
            game.update_from_engine()
