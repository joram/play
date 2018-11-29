import pytest
import datetime
from apps.tournament.models import TournamentGroup, Tournament, SnakeTournament, Snake, Team, TeamMember, User, UserSnake, SingleSnakePerTeamPerTournamentValidationError


def _arrange(num_snakes=10):
    tg = TournamentGroup.objects.create(name="test tournament group", date=datetime.datetime.now())
    t = Tournament.objects.create(name="test tournament", tournament_group=tg)
    snake = Snake.objects.create(name="Snake", id="snk_-1")
    team = Team.objects.create(name="test team", snake=snake)

    snakes = []
    for i in range(1, num_snakes+1):
        snake = Snake.objects.create(
            name="Snake {}".format(i),
            id="snk_{}".format(i)
        )
        user = User.objects.create(username="user_{}".format(i))
        TeamMember.objects.create(team=team, user=user)
        UserSnake.objects.create(snake=snake, user=user)
        snakes.append(snake)
    return snakes, t


def test_cant_add_two_snakes():
    snakes, tournament = _arrange()
    snake1 = snakes[0]
    snake2 = snakes[1]
    SnakeTournament.objects.create(tournament=tournament, snake=snake1)
    with pytest.raises(SingleSnakePerTeamPerTournamentValidationError):
        SnakeTournament.objects.create(tournament=tournament, snake=snake2)
