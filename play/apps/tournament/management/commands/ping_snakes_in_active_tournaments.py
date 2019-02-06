from django.core.management import BaseCommand

from apps.tournament.models import Tournament
from apps.snake.models import Snake


class Command(BaseCommand):
    help = "Ping all snakes in active tournaments"

    def handle(self, *args, **options):
        states = [Tournament.LOCKED, Tournament.IN_PROGRESS]
        snake_ids = []
        for tournament in Tournament.objects.filter(status__in=states):
            for bracket in tournament.brackets:
                for snake in bracket.snakes:
                    snake_ids.append(snake.id)
        snake_ids = set(snake_ids)

        for snake in Snake.objects.filter(id__in=snake_ids):
            ping_status_code = snake.ping()
            ok = ping_status_code == 200
            if not ok:
                print("snake {}'s ping was {}".format(snake.name, ping_status_code))
