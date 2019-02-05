import datetime

import pytest
from mock import mock

from apps.tournament.models import (
    TournamentBracket,
    Snake,
    Team,
    User,
    TeamMember,
    UserSnake,
    TournamentSnake,
    Tournament,
    RoundNotCompleteException,
)
from apps.utils.helpers import generate_game_url


def _arrange_tournament(name, num_snakes=8):
    tg = Tournament.objects.create(
        name="test tournament",
        date=datetime.datetime.now(),
        status=Tournament.REGISTRATION,
    )
    t = TournamentBracket.objects.create(name=name, tournament=tg)
    for i in range(1, num_snakes + 1):
        snake = Snake.objects.create(name=f"Snake {i}", id=f"snk_{i}")
        team = Team.objects.create(name="test team")
        user = User.objects.create(username=f"user_{i}")
        TeamMember.objects.create(team=team, user=user)
        UserSnake.objects.create(snake=snake, user=user)
        TournamentSnake.objects.create(tournament=tg, bracket=t, snake=snake)
    return t


def _mark_winner(game):
    game.status = game.Status.COMPLETE
    game.save()
    from apps.game.models import GameSnake

    marked_winner = False
    # Marks all snakes dead except the first one
    i = 0
    for gs in GameSnake.objects.filter(game=game).order_by("snake__id"):
        if not marked_winner:
            marked_winner = True
            continue
        gs.death = "snake-collision"
        gs.turns = i
        gs.save()
        i += 1


def _complete_games_in_round(r):
    for heat in r.heats:
        while heat.status != "complete":

            g1 = heat.create_next_game()
            _mark_winner(g1.game)


@pytest.mark.skip("something weird in here with how we access django objects")
def test_unable_to_create_next_round_until_all_heats_are_complete():
    bracket = _arrange_tournament("2 rounds", 24)
    print("create first round")
    bracket.create_next_round()

    with pytest.raises(RoundNotCompleteException):
        bracket.create_next_round()

    game = bracket.rounds[0].heats[0].create_next_game()
    _mark_winner(game.game)

    game = bracket.rounds[0].heats[0].create_next_game()
    _mark_winner(game.game)

    with pytest.raises(RoundNotCompleteException):
        bracket.create_next_round()

    game = bracket.rounds[0].heats[1].create_next_game()
    _mark_winner(game.game)
    game = bracket.rounds[0].heats[1].create_next_game()
    _mark_winner(game.game)
    game = bracket.rounds[0].heats[2].create_next_game()
    _mark_winner(game.game)
    game = bracket.rounds[0].heats[2].create_next_game()
    _mark_winner(game.game)

    # this should not throw an exception now that all games have been run
    bracket.create_next_round()


def test_create_next_round_partial_single_heat():
    bracket = _arrange_tournament("single heat", 5)
    bracket.create_next_round()

    rows = bracket.export()

    expected_rows = [
        [
            "Round",
            "Heat",
            "Snake Name",
            "Snake Id",
            "Game 1 URL",
            "Game 2 URL",
            "Game 3 URL",
        ],
        ["Round 1", "Heat 1", "Snake 1", "snk_1"],
        ["Round 1", "Heat 1", "Snake 2", "snk_2"],
        ["Round 1", "Heat 1", "Snake 3", "snk_3"],
        ["Round 1", "Heat 1", "Snake 4", "snk_4"],
        ["Round 1", "Heat 1", "Snake 5", "snk_5"],
    ]
    assert bracket.game_details() == []
    assert rows == expected_rows


@mock.patch("apps.game.models.Game.update_from_engine")
def test_bracket_with_2_snakes(update_mock):
    bracket = _arrange_tournament("single heat", 2)

    round1 = bracket.create_next_round()
    assert bracket.winners == False
    _complete_games_in_round(round1)

    g1 = round1.heats[0].games[0]
    g2 = round1.heats[0].games[1]
    bracket.cached_rounds = None

    assert round1.status == "complete"
    assert len(bracket.winners) == 2
    assert bracket.winners == [g1.winner.snake, g2.winner.snake]


@mock.patch("apps.game.models.Game.update_from_engine")
def test_bracket_with_3_snakes(update_mock):
    bracket = _arrange_tournament("single heat", 3)

    round1 = bracket.create_next_round()
    _complete_games_in_round(round1)

    g1 = round1.heats[0].games[0]
    g2 = round1.heats[0].games[1]
    g3 = round1.heats[0].games[2]
    assert round1.status == "complete"
    assert len(bracket.winners) == 3
    assert bracket.winners == [g1.winner.snake, g2.winner.snake, g3.winner.snake]


@mock.patch("apps.game.models.Game.update_from_engine")
def test_bracket_with_4_snakes(update_mock):
    bracket = _arrange_tournament("single heat", 4)

    round1 = bracket.create_next_round()
    _complete_games_in_round(round1)

    g1 = round1.heats[0].games[0]
    g2 = round1.heats[0].games[1]
    g3 = round1.heats[0].games[2]

    assert round1.status == "complete"
    assert len(bracket.winners) == 3
    assert bracket.winners == [g1.winner.snake, g2.winner.snake, g3.winner.snake]
    expected_runner_ups = [
        gs.snake for gs in g3.game.get_snakes().exclude(snake_id=g3.winner.snake.id)
    ]
    assert bracket.runner_ups == expected_runner_ups


@mock.patch("apps.game.models.Game.update_from_engine")
def test_bracket_with_8_snakes(update_mock):
    bracket = _arrange_tournament("single heat", 8)

    round1 = bracket.create_next_round()
    _complete_games_in_round(round1)

    g1 = round1.heats[0].games[0]
    g2 = round1.heats[0].games[1]
    g3 = round1.heats[0].games[2]

    assert round1.status == "complete"
    assert len(bracket.winners) == 3
    assert bracket.winners == [g1.winner.snake, g2.winner.snake, g3.winner.snake]
    expected_runner_ups = [
        gs.snake for gs in g3.game.get_snakes().exclude(snake_id=g3.winner.snake.id)
    ]
    assert bracket.runner_ups == expected_runner_ups


@mock.patch("apps.game.models.Game.update_from_engine")
def test_bracket_with_9_snakes(update_mock):
    bracket = _arrange_tournament("single heat", 9)

    round1 = bracket.create_next_round()
    _complete_games_in_round(round1)
    round2 = bracket.create_next_round()
    _complete_games_in_round(round2)

    g1 = round2.heats[0].games[0]
    g2 = round2.heats[0].games[1]
    g3 = round2.heats[0].games[2]

    assert round1.status == "complete"
    assert round2.status == "complete"
    assert len(bracket.winners) == 3
    assert bracket.winners == [g1.winner.snake, g2.winner.snake, g3.winner.snake]
    expected_runner_ups = [
        gs.snake for gs in g3.game.get_snakes().exclude(snake_id=g3.winner.snake.id)
    ]
    assert bracket.runner_ups == expected_runner_ups


@mock.patch("apps.game.models.Game.update_from_engine")
def test_bracket_with_24_snakes(update_mock):
    bracket = _arrange_tournament("single heat", 24)

    round1 = bracket.create_next_round()
    _complete_games_in_round(round1)
    round2 = bracket.create_next_round()
    _complete_games_in_round(round2)

    g1 = round2.heats[0].games[0]
    g2 = round2.heats[0].games[1]
    g3 = round2.heats[0].games[2]

    assert round1.status == "complete"
    assert round2.status == "complete"
    assert len(bracket.winners) == 3
    assert bracket.winners == [g1.winner.snake, g2.winner.snake, g3.winner.snake]
    expected_runner_ups = [
        gs.snake for gs in g3.game.get_snakes().exclude(snake_id=g3.winner.snake.id)
    ]
    assert bracket.runner_ups == expected_runner_ups


@pytest.mark.skip("something weird in here with how we access django objects")
@mock.patch("apps.game.models.Game.update_from_engine")
def test_bracket_with_25_snakes(update_mock):
    bracket = _arrange_tournament("single heat", 25)

    round1 = bracket.create_next_round()
    _complete_games_in_round(round1)
    round2 = bracket.create_next_round()
    _complete_games_in_round(round2)
    round3 = bracket.create_next_round()
    _complete_games_in_round(round3)

    g1 = round3.heats[0].games[0]
    g2 = round3.heats[0].games[1]
    g3 = round3.heats[0].games[2]
    assert round1.status == "complete"
    assert round2.status == "complete"
    assert round3.status == "complete"
    assert len(bracket.winners) == 3
    assert bracket.winners == [g1.winner.snake, g2.winner.snake, g3.winner.snake]
    expected_runner_ups = [
        gs.snake for gs in g3.game.get_snakes().exclude(snake_id=g3.winner.snake.id)
    ]
    assert bracket.runner_ups == expected_runner_ups


@mock.patch("apps.game.models.Game.update_from_engine")
def test_bracket_with_96_snakes(update_mock):
    bracket = _arrange_tournament("single heat", 96)

    round1 = bracket.create_next_round()
    _complete_games_in_round(round1)
    round2 = bracket.create_next_round()
    _complete_games_in_round(round2)
    round3 = bracket.create_next_round()
    _complete_games_in_round(round3)


    g1 = round3.heats[0].games[0]
    g2 = round3.heats[0].games[1]
    g3 = round3.heats[0].games[2]
    assert round1.status == "complete"
    assert round2.status == "complete"
    assert round3.status == "complete"
    assert len(bracket.winners) == 3
    assert bracket.winners == [g1.winner.snake, g2.winner.snake, g3.winner.snake]
    expected_runner_ups = [
        gs.snake for gs in g3.game.get_snakes().exclude(snake_id=g3.winner.snake.id)
    ]
    assert bracket.runner_ups == expected_runner_ups


@mock.patch("apps.game.models.Game.update_from_engine")
def test_bracket_with_97_snakes(update_mock):
    bracket = _arrange_tournament("single heat", 97)

    round1 = bracket.create_next_round()
    _complete_games_in_round(round1)
    round2 = bracket.create_next_round()
    _complete_games_in_round(round2)
    round3 = bracket.create_next_round()
    _complete_games_in_round(round3)
    round4 = bracket.create_next_round()
    _complete_games_in_round(round4)

    g1 = round4.heats[0].games[0]
    g2 = round4.heats[0].games[1]
    g3 = round4.heats[0].games[2]
    assert round1.status == "complete"
    assert round2.status == "complete"
    assert round3.status == "complete"
    assert round4.status == "complete"
    assert len(bracket.winners) == 3
    assert bracket.winners == [g1.winner.snake, g2.winner.snake, g3.winner.snake]
    expected_runner_ups = [
        gs.snake for gs in g3.game.get_snakes().exclude(snake_id=g3.winner.snake.id)
    ]
    assert bracket.runner_ups == expected_runner_ups
