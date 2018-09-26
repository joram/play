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

    def build_structure(self):
        numSnakes = Snake.objects.all().count()
        while numSnakes < 40:
            snake = random.choice(list(Snake.objects.all()))
            snake.id = None
            import names
            snake.name = names.get_full_name()
            snake.save()
            numSnakes += 1

        for snake in Snake.objects.all():  # update later
            print("adding %s to tournament %s" % (snake.name, self.name))
            SnakeTournament.objects.create(snake=snake, tournament=self)
        round = Round.objects.create(number=1, tournament=self)
        round.create_heats()

    @property
    def rounds(self):
        rounds = Round.objects.filter(tournament=self)
        print("rounds: %s" % rounds)
        return list(rounds)

    @property
    def snakes(self):
        snake_tournaments = SnakeTournament.objects.filter(tournament=self)
        snakes = []
        for st in snake_tournaments:
            snakes.append(st.snake)
        return snakes

    class Meta:
        app_label = 'tournament'


class SnakeTournament(models.Model):
    snake = models.ForeignKey(Snake, on_delete=models.CASCADE)
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

    @property
    def heats(self):
        return Heat.objects.filter(round=self)

    def create_heats(self, max_snakes_per=8):
        num_snakes = int(math.ceil(len(self.snakes)/max_snakes_per))
        heats = [Heat.objects.create(number=i+1, round=self) for i in range(0, num_snakes)]
        i = 0
        for snake in self.snakes:
            heat = heats[i % len(heats)]
            snakeTournament = SnakeTournament.objects.get(snake=snake, tournament=self.tournament)
            SnakeHeat.objects.create(snake=snakeTournament, heat=heat)
            i += 1

    class Meta:
        app_label = 'tournament'
        unique_together = (('number', 'tournament'))


class Heat(models.Model):
    number = models.IntegerField(default=1)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)

    @property
    def snakes(self):
        snakeHeats = SnakeHeat.objects.filter(heat=self)
        return [sh.snake.snake for sh in snakeHeats]

    @property
    def games(self):
        return HeatGame.objects.filter(heat=self)

    def create_next_game(self):
        n = self.games.count() + 1
        HeatGame.objects.create(heat=self, number=n)

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
