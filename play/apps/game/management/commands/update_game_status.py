from django.core.management.base import BaseCommand
from apps.game.jobs import GameStatusJob


class Command(BaseCommand):
    help = "Update game status"

    def handle(self, *args, **options):
        print("updating all game statuses")
        GameStatusJob().run()
