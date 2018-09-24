import math
import random
from django.db import models

from util.fields import ShortUUIDField
from apps.authentication.models import User
from apps.snake.models import Snake


class Team(models.Model):
    id = ShortUUIDField(prefix="tem", max_length=128, primary_key=True)
    name = models.CharField(max_length=128)
    description = models.TextField()
    snake = models.ForeignKey(Snake, on_delete=models.CASCADE)

    class Meta:
        app_label = 'tournament'


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)

    class Meta:
        app_label = 'tournament'
        unique_together = (('team', 'user'))


class Tournament(models.Model):
    name = models.CharField(max_length=256)

    def create(self):
        tournament = Tournament.objects.create()
        for snake in Snake.objects.all():  # update later
            SnakeTournament.objects.create(snake=snake, tournament=tournament)
        return tournament

    @property
    def snakes(self):
        snake_tournaments = SnakeTournament.objects.filter(tournament=self)
        snakes = []
        for st in snake_tournaments:
            snakes.append(st.snake)

    def create_round(self, round_num=1):
        round = Round.objects.create(number=round_num, tournament=self)
        round.create_heats()

    class Meta:
        app_label = 'tournament'


class SnakeTournament(models.Model):
    snake = models.ForeignKey(Snake, on_delete=models.CASCADE, unique=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    class Meta:
        app_label = 'tournament'
        unique_together = (('snake', 'tournament'))


class Round(models.Model):
    number = models.IntegerField(default=1)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    @property
    def previous(self):
        return Round.objects.get(number=self.number-1, tournament=self.tournament)

    @property
    def snakes(self):
        if self.number == 1:
            return self.tournament.snakes
        return self.previous.winners

    @property
    def winners(self):
        return self.snakes  # TODO: actually do

    def create_heats(self, max_snakes_per=8):
        num_snakes = int(math.ceil(len(self.snakes)/max_snakes_per))
        heats = [Heat.objects.create(number=i+1, round=self) for i in range(0, num_snakes)]
        i = 0
        for snake in self.snakes:
            heat = heats[i % len(heats)]
            SnakeHeat.objects.create(snake=snake, heat=heat)
            i += 1

    class Meta:
        app_label = 'tournament'
        unique_together = (('number', 'tournament'))


class Heat(models.Model):
    number = models.IntegerField(default=1)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)

    @property
    def snakes(self):
        snakes = []
        for snake_heat in SnakeHeat.objects.get(heat=self):
            snakes.append(snake_heat.snake)
        return snakes

    class Meta:
        app_label = 'tournament'


class HeatGame(models.Model):
    number = models.IntegerField(default=1)
    heat = models.ForeignKey(Heat, on_delete=models.CASCADE)

    @property
    def snakes(self):
        if self.number == 1:
            return self.heat.snakes

    @property
    def winner(self):
        return random.choice(self.snakes)  # TODO: do properly


class SnakeHeat(models.Model):
    heat = models.ForeignKey(Heat, on_delete=models.CASCADE)
    snake = models.ForeignKey(SnakeTournament, on_delete=models.CASCADE)

    class Meta:
        app_label = 'tournament'
        unique_together = (('heat', 'snake'))
