import math
from django.db import models
from django.core.exceptions import ValidationError

from apps.snake.models import Snake, UserSnake
from apps.tournament.models.teams import TeamMember
from apps.utils.helpers import generate_game_url


class SingleSnakePerTeamPerTournamentValidationError(ValidationError):

    def __init__(self):
        super().__init__(message='Only one snake per event per team')


class TournamentClosedValidationError(ValidationError):

    def __init__(self):
        super().__init__(message='Tournament over')


class PreviousGameNotCompleteValidationError(ValidationError):

    def __init__(self):
        super().__init__(message='The previous game is not complete')


class Tournament(models.Model):
    LOCKED = 'LO'  # Not started, but nobody can register
    HIDDEN = 'HI'  # Able to add snakes manually (invite-only)
    REGISTRATION = 'RE'  # Publicly viewable and opt-in-able
    IN_PROGRESS = 'PR'
    COMPLETE = 'JR'
    STATUSES = (
        (LOCKED, 'Locked'),
        (HIDDEN, 'Hidden'),
        (REGISTRATION, 'Registration'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETE, 'Complete'),
    )
    status = models.CharField(max_length=2, choices=STATUSES, default=LOCKED)
    single_snake_per_team = models.BooleanField(default=True)
    name = models.CharField(max_length=256)
    date = models.DateField()
    snakes = models.ManyToManyField(
        Snake, through="TournamentSnake", through_fields=("tournament", "snake")
    )

    @property
    def brackets(self):
        return TournamentBracket.objects.filter(tournament=self)

    def __str__(self):
        return f'{self.name}'


class TournamentBracket(models.Model):
    name = models.CharField(max_length=256)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    snakes = models.ManyToManyField(
        Snake, through="TournamentSnake", through_fields=("bracket", "snake")
    )

    header_row = [
        "Round",
        "Heat",
        "Snake Name",
        "Snake Id",
        "Game 1 URL",
        "Game 2 URL",
        "Game 3 URL",
    ]

    def create_next_round(self):
        if self.latest_round is not None and self.latest_round.status != "complete":
            raise Exception("can't create next round")

        num = max([r.number for r in self.rounds]+[0])+1
        return Round.objects.create(number=num, tournament_bracket=self)

    @property
    def rounds(self):
        rounds = Round.objects.filter(tournament_bracket=self).order_by("number")
        return list(rounds)

    @property
    def latest_round(self):
        rounds = self.rounds
        if len(rounds) == 0:
            return None
        return rounds[0]

    @property
    def snake_count(self):
        return self.snakes.count()

    def game_details(self):
        games = []
        for round in self.rounds:
            for heat in round.heats:
                for hg in heat.games:
                    status = hg.game.status if hg.game is not None else None
                    games.append({
                        "id": hg.game.id,
                        "url": generate_game_url(hg.game.engine_id),
                        "status": status,
                        "round": round.number,
                        "heat": heat.number,
                        "heat_game": hg.number,
                    })
        return games

    def export(self):
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

    def __str__(self):
        return f'{self.name}'

    class Meta:
        app_label = 'tournament'


class TournamentSnake(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    snake = models.ForeignKey(Snake, on_delete=models.CASCADE)
    bracket = models.ForeignKey(TournamentBracket, null=True, on_delete=models.SET_NULL)

    class Meta:
        app_label = 'tournament'

# <<<<<<< HEAD
#         app_label = 'tournament'
#         unique_together = (
#             ('snake', 'tournament_bracket'),
#         )
#
#     def validate_unique(self, exclude=None):
#         user_snake = UserSnake.objects.get(snake=self.snake)
#         team_member = TeamMember.objects.get(user=user_snake.user)
#         team = team_member.team
#         tournament = self.tournament_bracket.tournament
#
#         if tournament.status in [Tournament.LOCKED, Tournament.IN_PROGRESS, Tournament.COMPLETE]:
#             raise TournamentClosedValidationError()
#
#         tournament_brackets = TournamentBracket.objects.filter(tournament=self.tournament_bracket.tournament)
#         qs = SnakeTournamentBracket.objects.filter(snake__in=team.snakes, tournament_bracket__in=tournament_brackets)
#         if tournament.single_snake_per_team:
#             if qs.count() > 1:
#                 raise SingleSnakePerTeamPerTournamentValidationError()
#             if qs.count() == 1 and qs[0] != self:
#                 raise SingleSnakePerTeamPerTournamentValidationError()
#
#         models.Model.validate_unique(self, exclude=exclude)
#
#     def save(self, *args, **kwargs):
#         self.validate_unique()
#         super(SnakeTournamentBracket, self).save(*args, **kwargs)
#
# =======

class RoundManager(models.Manager):
    def create(self, *args, **kwargs):
        round = super(RoundManager, self).create(*args, **kwargs)
        max_snakes_per = 8

        # Finale
        if len(round.snakes) <= 3:
            print("making finals")
            heat = Heat.objects.create(number=1, round=round, desired_games=1)
            print(round.snakes)
            for snake in round.snakes:
                SnakeHeat.objects.create(snake=snake, heat=heat)
            return round

        # Semi-Finals (picking top 3)
        if len(round.snakes) < max_snakes_per:
            print("making semi-finals")
            heat = Heat.objects.create(number=1, round=round, desired_games=3)
            for snake in round.snakes:
                SnakeHeat.objects.create(snake=snake, heat=heat)
            return round

        # Reduction
        num_heats = int(math.ceil(len(round.snakes)/max_snakes_per))
        heats = [Heat.objects.create(number=i+1, round=round) for i in range(0, num_heats)]
        i = 0
        for snake in round.snakes:
            heat = heats[i % len(heats)]
            SnakeHeat.objects.create(snake=snake, heat=heat)
            i += 1
        return round


class Round(models.Model):
    number = models.IntegerField(default=1)
    tournament_bracket = models.ForeignKey(TournamentBracket, on_delete=models.CASCADE)
    objects = RoundManager()

    @property
    def previous(self):
        return Round.objects.get(number=self.number-1, tournament_bracket=self.tournament_bracket)

    @property
    def snakes(self):
        if self.number == 1:
            return [s for s in self.tournament_bracket.snakes.all()]
        return [s.snake for s in self.previous.winners]

    @property
    def winners(self):
        winners = []
        for heat in self.heats:
            winners += heat.winners
        return winners

    @property
    def heats(self):
        return Heat.objects.filter(round=self)

    @property
    def status(self):
        for heat in self.heats:
            if heat.status is not "complete":
                return heat.status
        return "complete"

    class Meta:
        app_label = 'tournament'
        unique_together = ('number', 'tournament_bracket')


class Heat(models.Model):
    number = models.IntegerField(default=1)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    desired_games = models.IntegerField(default=2)

    @property
    def snakes(self):
        snakeHeats = SnakeHeat.objects.filter(heat=self)
        snakes = [sh.snake for sh in snakeHeats]
        return snakes

    @property
    def games(self):
        qs = HeatGame.objects.filter(heat=self)
        return qs

    @property
    def latest_game(self):
        hgs = HeatGame.objects.filter(heat=self).order_by("-number")
        if len(hgs) == 0:
            return None
        return hgs[0]

    @property
    def winners(self):
        winners = []
        for game in self.games:
            print("heat {}, game {} has winnner {}".format(
                self.number,
                game.number,
                game.winner.snake.id,
            ))
            winners.append(game.winner)

        return winners

    @property
    def status(self):
        for hg in self.games:
            hg.game.update_from_engine()
        if len(self.games) < self.desired_games:
            return "running"
        for game in self.games:
            if game.status is not "complete":
                return game.status
        return "complete"

    def create_next_game(self):
        if len(self.games) >= self.desired_games:
            raise PreviousGameNotCompleteValidationError()

        n = self.games.count() + 1
        if self.latest_game is not None and self.latest_game.status != "complete":
            raise PreviousGameNotCompleteValidationError()
        return HeatGame.objects.create(heat=self, number=n)

    class Meta:
        app_label = 'tournament'


class HeatGameManager(models.Manager):
    def create(self, *args, **kwargs):
        heat = kwargs.get("heat")
        previous_game = heat.latest_game
        skip = [w.snake.id for w in heat.winners]
        print(skip)
        if previous_game is not None:
            skip.append(previous_game.winner.snake.id)
            next_snakes = [s for s in previous_game.snakes if s.id not in skip]
        else:
            next_snakes = heat.snakes
        snake_ids = [{"id": snake.id} for snake in next_snakes]

        from apps.game.models import Game
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
        previous_hgs = HeatGame.objects.filter(heat=self.heat, number__lt=self.number)
        previous_winners = [hg.winner for hg in previous_hgs if hg.winner is not None]
        previous_winners_ids = [w.id for w in previous_winners]
        snakes = [s for s in self.heat.snakes if s.id not in previous_winners_ids]
        return snakes

    @property
    def winner(self):
        return self.game.winner()

    @property
    def status(self):
        return self.game.status

    @property
    def previous(self):
        if self.number == 1:
            return None
        return HeatGame.objects.get(number=self.number-1, heat=self.heat)


class SnakeHeat(models.Model):
    heat = models.ForeignKey(Heat, on_delete=models.CASCADE)
    snake = models.ForeignKey(Snake, on_delete=models.CASCADE)

    class Meta:
        app_label = 'tournament'
        unique_together = (('heat', 'snake'))

