from django.db import models

from util.fields import ShortUUIDField
from apps.authentication.models import User
from apps.snake.models import Snake, UserSnake


class Team(models.Model):
    id = ShortUUIDField(prefix="tem", max_length=128, primary_key=True)
    name = models.CharField(max_length=128)
    description = models.TextField()
    snake = models.ForeignKey(Snake, on_delete=models.CASCADE)

    @property
    def snakes(self):
        users = [tm.user for tm in TeamMember.objects.filter(team=self)]
        snakes = [us.snake for us in UserSnake.objects.filter(user__in=users)]
        return snakes

    @property
    def tournament_snakes(self):
        from apps.tournament.models import TournamentSnake
        return TournamentSnake.objects.filter(snake__in=self.snakes)

    @property
    def available_tournaments(self):
        from apps.tournament.models import Tournament
        return Tournament.objects.filter(status=Tournament.REGISTRATION).exclude(id__in=[ts.tournament.id for ts in self.tournament_snakes])

    class Meta:
        app_label = "tournament"


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)

    class Meta:
        app_label = "tournament"
        unique_together = ("team", "user")
