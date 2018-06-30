from apps.game.models import Game


class GameStatusJob:
    active_statuses = (
        Game.Status.PENDING,
        Game.Status.RUNNING,
        Game.Status.STOPPED,
    )

    def run(self):
        for game in Game.objects.filter(status__in=self.active_statuses):
            game.update_from_engine()
