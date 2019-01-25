import pytest
import datetime
from apps.tournament.models import Tournament, TournamentBracket, SnakeTournamentBracket, Snake, Team, TeamMember, User, UserSnake, SingleSnakePerTeamPerTournamentValidationError


def _arrange(num_snakes=10):
    tournament = Tournament.objects.create(name="test tournament", date=datetime.datetime.now())
    tournament_brackets = []
    for i in range(0, 3):
        t = TournamentBracket.objects.create(name="test tournament {}".format(i), tournament=tournament)
        tournament_brackets.append(t)
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
    return snakes, tournament, tournament_brackets


def test_cant_add_two_snakes_to_the_same_tournament():
    snakes, tournament, tournament_brackets = _arrange()
    snake1 = snakes[0]
    snake2 = snakes[1]
    SnakeTournamentBracket.objects.create(tournament_bracket=tournament_brackets[0], snake=snake1)
    with pytest.raises(SingleSnakePerTeamPerTournamentValidationError):
        SnakeTournamentBracket.objects.create(tournament_bracket=tournament_brackets[0], snake=snake2)


def test_cant_add_two_snakes_to_different_tournament_brackets():
    snakes, tournament, tournament_brackets = _arrange()
    snake1 = snakes[0]
    snake2 = snakes[1]
    SnakeTournamentBracket.objects.create(tournament_bracket=tournament_brackets[0], snake=snake1)
    with pytest.raises(SingleSnakePerTeamPerTournamentValidationError):
        SnakeTournamentBracket.objects.create(tournament_bracket=tournament_brackets[1], snake=snake2)


def test_cant_add_same_snake_to_different_tournament_brackets():
    snakes, tournament, tournament_brackets = _arrange()
    snake1 = snakes[0]
    SnakeTournamentBracket.objects.create(tournament_bracket=tournament_brackets[0], snake=snake1)
    with pytest.raises(SingleSnakePerTeamPerTournamentValidationError):
        SnakeTournamentBracket.objects.create(tournament_bracket=tournament_brackets[1], snake=snake1)


def test_can_add_two_snakes_to_the_same_tournament():
    snakes, tournament, tournament_brackets = _arrange()
    tournament.single_snake_per_team = False
    tournament.save()
    snake1 = snakes[0]
    snake2 = snakes[1]
    SnakeTournamentBracket.objects.create(tournament_bracket=tournament_brackets[0], snake=snake1)

    # shouldn't raise an exception
    SnakeTournamentBracket.objects.create(tournament_bracket=tournament_brackets[0], snake=snake2)


def test_can_add_two_snakes_to_different_tournament_brackets():
    snakes, tournament, tournament_brackets = _arrange()
    tournament.single_snake_per_team = False
    tournament.save()
    snake1 = snakes[0]
    snake2 = snakes[1]
    SnakeTournamentBracket.objects.create(tournament_bracket=tournament_brackets[0], snake=snake1)

    # shouldn't raise an exception
    SnakeTournamentBracket.objects.create(tournament_bracket=tournament_brackets[1], snake=snake2)


def test_can_add_same_snake_to_different_tournament_brackets():
    snakes, tournament, tournament_brackets = _arrange()
    snake1 = snakes[0]
    tournament.single_snake_per_team = False
    tournament.save()
    SnakeTournamentBracket.objects.create(tournament_bracket=tournament_brackets[0], snake=snake1)

    # shouldn't raise an exception
    SnakeTournamentBracket.objects.create(tournament_bracket=tournament_brackets[1], snake=snake1)
