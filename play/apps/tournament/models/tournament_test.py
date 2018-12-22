import pytest
import datetime
from apps.tournament.models import Tournament, TournamentBracket, Snake, Team, TeamMember, User, UserSnake, SingleSnakePerTeamPerTournamentValidationError


def _arrange(num_snakes=10):
    tg = Tournament.objects.create(name="test tournament", date=datetime.datetime.now())
    tournaments = []
    for i in range(0, 3):
        t = TournamentBracket.objects.create(name="test tournament {}".format(i), tournament=tg)
        tournaments.append(t)
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
    return snakes, tournaments
