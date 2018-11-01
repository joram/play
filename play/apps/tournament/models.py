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
    header_row = ["Round", "Heat", "Snake Name", "Snake Id", "Game 1 URL", "Game 2 URL"]

    def build_structure(self):
        round = Round.objects.create(number=1, tournament=self)
        round.create_heats()

    @property
    def rounds(self):
        rounds = Round.objects.filter(tournament=self)
        return list(rounds)

    @property
    def snakes(self):
        snake_tournaments = SnakeTournament.objects.filter(tournament=self)
        snakes = []
        for st in snake_tournaments:
            snakes.append(st.snake)
        return snakes

    def get_csv(self):
        rows = [self.header_row]
        for round in self.rounds:
            for heat in round.heats:
                for snake in heat.snakes:
                    row = [
                        "Round {}".format(round.number),
                        "Heat {}".format(heat.number),
                        snake.name,
                        snake.id,
                    ]
                    for heat_game in heat.games:
                        row.append("https://play.battlesnake.io/game/{}".format(heat_game.game.id))
                    rows.append(row)
        return rows

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
        return HeatGame.objects.create(heat=self, number=n)

    class Meta:
        app_label = 'tournament'


class HeatGameManager(models.Manager):

    def create(self, *args, **kwargs):
        from apps.game.models import Game
        snake_ids = []
        game = Game(width=20, height=20, food=10, snakes=snake_ids)
        game.create()
        game.save()
        return super(HeatGameManager, self).create(*args, **kwargs, game=game)


class HeatGame(models.Model):
    number = models.IntegerField(default=1)
    heat = models.ForeignKey(Heat, on_delete=models.CASCADE)
    game = models.ForeignKey('game.Game', on_delete=models.DO_NOTHING)
    objects = HeatGameManager()

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
