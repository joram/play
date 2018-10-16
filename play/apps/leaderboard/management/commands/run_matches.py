from django.core.management.base import BaseCommand
from apps.leaderboard.jobs import MatchStarter


class Command(BaseCommand):
    help = "Run leaderboard matches"

    def handle(self, *args, **options):
        print("running leaderboard matches")
        MatchStarter().run()
