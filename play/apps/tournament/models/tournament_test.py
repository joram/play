import pytest
import datetime
from apps.tournament.models import Tournament, TournamentBracket, SnakeTournamentBracket, Snake, Team, TeamMember, User, UserSnake, SingleSnakePerTeamPerTournamentValidationError


def _arrange(num_snakes=10):
    tg = Tournament.objects.create(name="test tournament group", date=datetime.datetime.now())
    tournnaments = []
    for i in range(0, 3):
        t = TournamentBracket.objects.create(name="test tournament {}".format(i), tournament_group=tg)
        tournnaments.append(t)
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
    return snakes, tournnaments


def test_cant_add_two_snakes_to_the_same_tournament():
    snakes, tournaments = _arrange()
    snake1 = snakes[0]
    snake2 = snakes[1]
    SnakeTournamentBracket.objects.create(tournament=tournaments[0], snake=snake1)
    with pytest.raises(SingleSnakePerTeamPerTournamentValidationError):
        SnakeTournamentBracket.objects.create(tournament=tournaments[0], snake=snake2)


def test_cant_add_two_snakes_to_different_tournaments():
    snakes, tournaments = _arrange()
    snake1 = snakes[0]
    snake2 = snakes[1]
    SnakeTournamentBracket.objects.create(tournament=tournaments[0], snake=snake1)
    with pytest.raises(SingleSnakePerTeamPerTournamentValidationError):
        SnakeTournamentBracket.objects.create(tournament=tournaments[1], snake=snake2)


def test_cant_add_same_snake_to_different_tournaments():
    snakes, tournaments = _arrange()
    snake1 = snakes[0]
    SnakeTournamentBracket.objects.create(tournament=tournaments[0], snake=snake1)
    with pytest.raises(SingleSnakePerTeamPerTournamentValidationError):
        SnakeTournamentBracket.objects.create(tournament=tournaments[1], snake=snake1)
