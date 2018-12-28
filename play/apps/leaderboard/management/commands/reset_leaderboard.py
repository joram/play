from django.core.management import BaseCommand

from apps.leaderboard.models import UserSnakeLeaderboard, LeaderboardResult


class Command(BaseCommand):
    help = "Reset Leaderboard"

    def handle(self, *args, **options):
        print("resets rankings for all snakes")
        for lb in UserSnakeLeaderboard.objects.all():
            lb.sigma = None
            lb.mu = None
            lb.save()

        LeaderboardResult.objects.all().delete()
