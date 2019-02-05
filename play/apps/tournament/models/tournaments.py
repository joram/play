import math

from django.core.exceptions import ValidationError
from django.db import models

from apps.snake.models import Snake
from apps.utils.helpers import generate_game_url


class PreviousGameTiedException(ValidationError):
    def __init__(self):
        super().__init__(message="Previous game ended in a tie.")


class SingleSnakePerTeamPerTournamentValidationError(ValidationError):
    def __init__(self):
        super().__init__(message="Only one snake per event per team")


class TournamentClosedValidationError(ValidationError):
    def __init__(self):
        super().__init__(message="Tournament over")


class DesiredGamesReachedValidationError(ValidationError):
    def __init__(self):
        super().__init__(message="No more games should be run for this heat")


class RoundNotCompleteException(ValidationError):
    def __init__(self):
        super().__init__(message="Complete all games before creating next round.")


class Tournament(models.Model):
    LOCKED = "LO"  # Not started, but nobody can register
    HIDDEN = "HI"  # Able to add snakes manually (invite-only)
    REGISTRATION = "RE"  # Publicly viewable and opt-in-able
    IN_PROGRESS = "PR"
    COMPLETE = "JR"
    STATUSES = (
        (LOCKED, "Locked"),
        (HIDDEN, "Hidden"),
        (REGISTRATION, "Registration"),
        (IN_PROGRESS, "In Progress"),
        (COMPLETE, "Complete"),
    )

    casting_uri = models.CharField(default="", max_length=1024)
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

    @property
    def is_registration_open(self):
        return self.status == self.REGISTRATION

    def __str__(self):
        return f"{self.name}"


class TournamentBracket(models.Model):

    name = models.CharField(max_length=256)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    board_width = models.IntegerField(default=11)
    board_height = models.IntegerField(default=11)
    board_food = models.IntegerField(default=2)
    board_max_turns_to_next_food_spawn = models.IntegerField(default=15)
    snakes = models.ManyToManyField(
        Snake, through="TournamentSnake", through_fields=("bracket", "snake")
    )

    cached_rounds = None

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
            raise RoundNotCompleteException

        num = max([r.number for r in self.rounds] + [0]) + 1
        self.cached_rounds = None  # clear out cached data
        return Round.objects.create(number=num, tournament_bracket=self)

    @property
    def rounds(self):
        if self.cached_rounds is None:
            self.cached_rounds = list(
                self.round_set.all()
                .prefetch_related(
                    "heat_set__heatgame_set__game", "heat_set__snakeheat_set__snake"
                )
                .order_by("number")
            )
        return self.cached_rounds

    @property
    def latest_round(self):
        if len(self.rounds) == 0:
            return None
        return self.rounds[0]

    @property
    def winners(self):
        if self.latest_round is None:
            return False
        if self.latest_round.heats.count() != 1:
            return False
        if self.latest_round.heats[0].games.count() != 1:
            return False
        if self.latest_round.status != "complete":
            return False

        final_game = self.latest_round.heats[0].games[0]
        final_game.game.ranked_snakes()

    @property
    def snake_count(self):
        return self.snakes.count()

    def game_details(self):
        games = []
        for r in self.rounds:
            for heat in r.heats:
                for hg in heat.games:
                    status = hg.game.status if hg.game is not None else None
                    games.append(
                        {
                            "id": hg.game.id,
                            "url": generate_game_url(hg.game.engine_id),
                            "status": status,
                            "round": r.number,
                            "heat": heat.number,
                            "heat_game": hg.number,
                        }
                    )
        return games

    def export(self):
        rows = [self.header_row]
        for r in self.rounds:
            for heat in r.heats:
                for snake_heat in heat.snakes:
                    row = [
                        f"Round {r.number}",
                        f"Heat {heat.number}",
                        snake_heat.snake.name,
                        snake_heat.snake.id,
                    ]
                    for heat_game in heat.games:
                        row.append(
                            f"https://play.battlesnake.io/game/{heat_game.game.engine_id}"
                        )
                    rows.append(row)
        return rows

    def __str__(self):
        return f"{self.name}"

    class Meta:
        app_label = "tournament"


class TournamentSnake(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    snake = models.ForeignKey(Snake, on_delete=models.CASCADE)
    bracket = models.ForeignKey(TournamentBracket, null=True, on_delete=models.SET_NULL)

    class Meta:
        app_label = "tournament"


class RoundManager(models.Manager):
    def create(self, *args, **kwargs):
        round = super(RoundManager, self).create(*args, **kwargs)
        max_snakes_per = 8
        num_snakes = len(round.snakes)
        # reduction round
        if num_snakes > 6 and round.tournament_bracket.tournament.snakes.count() > 8:

            # create heats
            num_heats = int(math.ceil(num_snakes / max_snakes_per))
            if 12 <= num_snakes <= 24:
                num_heats = 3
            if num_snakes > 24 and num_heats == 4:
                num_heats = 6
            heats = [
                Heat.objects.create(number=i + 1, round=round)
                for i in range(0, num_heats)
            ]

            i = 0
            for snake in round.snakes:
                SnakeHeat.objects.create(snake=snake, heat=heats[i % num_heats])
                i += 1

            return round

        # finals, TODO: this needs to be updated i think, desired_games should be 3?
        heat = Heat.objects.create(number=1, round=round, desired_games=1)
        for snake in round.snakes:
            SnakeHeat.objects.create(snake=snake, heat=heat)
        return round


class Round(models.Model):
    number = models.IntegerField(default=1)
    tournament_bracket = models.ForeignKey(TournamentBracket, on_delete=models.CASCADE)
    objects = RoundManager()

    @property
    def previous(self):
        return Round.objects.get(
            number=self.number - 1, tournament_bracket=self.tournament_bracket
        )

    @property
    def snakes(self):
        if self.number == 1:
            return [s for s in self.tournament_bracket.snakes.all()]
        return [s.snake for s in self.previous.winners]

    @property
    def snake_count(self):
        return len(self.snakes)

    @property
    def winners(self):
        winners = []
        for heat in self.heats:
            winners += heat.winners
        return winners

    @property
    def heats(self):
        return self.heat_set.all()

    @property
    def status(self):
        for heat in self.heats:
            if heat.status != "complete":
                return heat.status
        return "complete"

    class Meta:
        app_label = "tournament"
        unique_together = ("number", "tournament_bracket")


class Heat(models.Model):
    number = models.IntegerField(default=1)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    desired_games = models.IntegerField(default=2)

    @property
    def snakes(self):
        return self.snakeheat_set.all()

    @property
    def games(self):
        return self.heatgame_set.all()

    @property
    def latest_game(self):
        hgs = self.games.order_by("-number")
        if hgs.count() == 0:
            return None
        return hgs.first()

    @property
    def winners(self):
        winners = []
        for game in self.games:
            if game.winner is not None:
                winners.append(game.winner)
        return winners

    @property
    def status(self):
        if self.games.count() < self.desired_games:
            return "running"
        from apps.game.models import Game

        for hg in self.games:
            if hg.game.status is not Game.Status.COMPLETE:
                return hg.game.status
        return "complete"

    def create_next_game(self):
        if self.games.count() >= self.desired_games:
            raise DesiredGamesReachedValidationError()

        n = self.games.count() + 1
        from apps.game.models import Game

        if (
            self.latest_game is not None
            and self.latest_game.game.status != Game.Status.COMPLETE
        ):
            raise Exception("can't create next game")
        hg = HeatGame.objects.create(heat=self, number=n)
        return hg

    class Meta:
        app_label = "tournament"


class HeatGameManager(models.Manager):
    def create(self, *args, **kwargs):
        heat = kwargs.get("heat")
        previous_game = heat.latest_game
        skip = [w.snake.id for w in heat.winners]
        if previous_game is not None:
            if previous_game.winner is None:
                raise PreviousGameTiedException()
            skip.append(previous_game.winner.snake.id)
            next_snakes = [
                sh.snake for sh in previous_game.snakes if sh.snake.id not in skip
            ]
        else:
            next_snakes = [sh.snake for sh in heat.snakes]
        snake_ids = [{"id": snake.id} for snake in next_snakes]

        from apps.game.models import Game

        game = Game(
            width=heat.round.tournament_bracket.board_width,
            height=heat.round.tournament_bracket.board_height,
            food=heat.round.tournament_bracket.board_food,
            max_turns_to_next_food_spawn=heat.round.tournament_bracket.board_max_turns_to_next_food_spawn,
            snakes=snake_ids,
        )
        game.create()
        game.save()

        return super(HeatGameManager, self).create(*args, **kwargs, game=game)


class HeatGame(models.Model):
    UNWATCHED = "UW"
    WATCHING = "W"
    WATCHED = "WD"
    STATUSES = (
        (UNWATCHED, "Not Casted Yet"),
        (WATCHING, "Casting"),
        (WATCHED, "Casted"),
    )
    status = models.CharField(max_length=2, choices=STATUSES, default=UNWATCHED)
    number = models.IntegerField(default=1)
    heat = models.ForeignKey(Heat, on_delete=models.CASCADE)
    game = models.ForeignKey("game.Game", on_delete=models.DO_NOTHING)
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
        if not hasattr(self, "_winner") or self._winner is None:
            self._winner = self.game.winner()
        return self._winner

    @property
    def human_readable_status(self):
        for (short, name) in self.STATUSES:
            if self.status == short:
                return name

    @property
    def previous(self):
        if self.number == 1:
            return None
        return HeatGame.objects.get(number=self.number - 1, heat=self.heat)


class SnakeHeat(models.Model):
    heat = models.ForeignKey(Heat, on_delete=models.CASCADE)
    snake = models.ForeignKey(Snake, on_delete=models.CASCADE)

    @property
    def first(self):
        if self.heat.games.count() == 0:
            return False
        if self.heat.games[0].winner is None:
            return False
        return self.heat.games[0].winner.snake == self.snake

    @property
    def second(self):
        if self.heat.games.count() <= 1:
            return False
        if self.heat.games[1].winner is None:
            return False
        return self.heat.games[1].winner.snake == self.snake

    class Meta:
        app_label = "tournament"
        unique_together = ("heat", "snake")
