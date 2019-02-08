import datetime

import pytest
from mock import mock

from apps.tournament.models import (
    TournamentBracket,
    Snake,
    Team,
    User,
    Round,
    TeamMember,
    UserSnake,
    TournamentSnake,
    Tournament,
    RoundNotCompleteException,
)


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
    assert bracket.winners is False
    _complete_games_in_round(round1)

    g1 = round1.heats[0].games[0]
    bracket.cached_rounds = None

    assert round1.status == "complete"
    assert round1.heats[0].status == "complete"
    assert round1.name == Round.NAME_FINAL_2
    assert len(bracket.winners) == 1
    assert bracket.winners == [g1.winner.snake]
    expected_runner_ups = [gs.snake for gs in g1.game.get_snakes().exclude(snake_id=g1.winner.snake.id)]
    # assert bracket.runner_ups == expected_runner_ups


@mock.patch("apps.game.models.Game.update_from_engine")
def test_bracket_with_3_snakes(update_mock):
    bracket = _arrange_tournament("single heat", 3)
    round1 = bracket.create_next_round()
    _complete_games_in_round(round1)
    round2 = bracket.create_next_round()
    _complete_games_in_round(round2)

    assert round1.status == "complete"
    assert round1.heats[0].status == "complete"
    assert round1.name == Round.NAME_FINAL_3
    assert round2.name == Round.NAME_FINAL_2
    assert bracket.winners == [
        Snake.objects.get(name="Snake 1"),
        Snake.objects.get(name="Snake 2"),
        Snake.objects.get(name="Snake 3"),
    ]
    assert bracket.runner_ups == []


@mock.patch("apps.game.models.Game.update_from_engine")
def test_bracket_with_4_snakes(update_mock):
    bracket = _arrange_tournament("single heat", 4)

    round1 = bracket.create_next_round()
    _complete_games_in_round(round1)
    round2 = bracket.create_next_round()
    _complete_games_in_round(round2)
    round3 = bracket.create_next_round()
    _complete_games_in_round(round3)

    assert round1.status == "complete"
    assert round1.heats[0].status == "complete"
    assert round1.name == Round.NAME_FINAL_6
    assert round2.name == Round.NAME_FINAL_3
    assert round3.name == Round.NAME_FINAL_2
    assert len(bracket.winners) == 3
    assert bracket.winners == [
        Snake.objects.get(name="Snake 1"),
        Snake.objects.get(name="Snake 2"),
        Snake.objects.get(name="Snake 3"),
    ]
    assert bracket.runner_ups == [
        Snake.objects.get(name="Snake 4"),
    ]


@mock.patch("apps.game.models.Game.update_from_engine")
def test_bracket_with_8_snakes(update_mock):
    bracket = _arrange_tournament("single heat", 8)
    # Round1: 4 (2 games), 4 (2 games) -> 4 winners
    # Round2: 4 (3 games) -> 3 winners
    # Round3: 3 (2 games) -> 2 winners
    # Round4: 2 (1 game) -> 1 winner

    round1 = bracket.create_next_round()
    _complete_games_in_round(round1)
    round2 = bracket.create_next_round()
    _complete_games_in_round(round2)
    round3 = bracket.create_next_round()
    _complete_games_in_round(round3)

    assert round1.status == "complete"
    assert round1.heats[0].status == "complete"
    assert len(bracket.winners) == 3
    assert bracket.winners == [
        Snake.objects.get(name="Snake 1"),
        Snake.objects.get(name="Snake 2"),
        Snake.objects.get(name="Snake 3"),
    ]
    assert bracket.runner_ups == [
        Snake.objects.get(name="Snake 4"),
        Snake.objects.get(name="Snake 5"),
        Snake.objects.get(name="Snake 6"),
        Snake.objects.get(name="Snake 7"),
        Snake.objects.get(name="Snake 8"),
    ]


@mock.patch("apps.game.models.Game.update_from_engine")
def test_bracket_with_9_snakes(update_mock):
    bracket = _arrange_tournament("single heat", 9)

    round1 = bracket.create_next_round()
    _complete_games_in_round(round1)
    round2 = bracket.create_next_round()
    _complete_games_in_round(round2)
    round3 = bracket.create_next_round()
    _complete_games_in_round(round3)
    round4 = bracket.create_next_round()
    _complete_games_in_round(round4)

    assert round1.status == "complete"
    assert round1.heats[0].status == "complete"
    assert round1.heats[1].status == "complete"
    assert round2.status == "complete"
    assert round2.heats[0].status == "complete"
    assert len(bracket.winners) == 3
    assert bracket.winners == [
        Snake.objects.get(name="Snake 1"),
        Snake.objects.get(name="Snake 2"),
        Snake.objects.get(name="Snake 3"),
    ]
    assert bracket.runner_ups == [
        Snake.objects.get(name="Snake 4"),
    ]


@mock.patch("apps.game.models.Game.update_from_engine")
def test_bracket_with_24_snakes(update_mock):
    bracket = _arrange_tournament("single heat", 24)

    round1 = bracket.create_next_round()
    _complete_games_in_round(round1)
    round2 = bracket.create_next_round()
    _complete_games_in_round(round2)
    round3 = bracket.create_next_round()
    _complete_games_in_round(round3)
    round4 = bracket.create_next_round()
    _complete_games_in_round(round4)

    assert round1.status == "complete"
    assert round2.status == "complete"
    assert len(bracket.winners) == 3
    assert bracket.winners == [
        Snake.objects.get(name="Snake 1"),
        Snake.objects.get(name="Snake 10"),
        Snake.objects.get(name="Snake 11"),
    ]
    assert bracket.runner_ups == [
        Snake.objects.get(name="Snake 14"),
        Snake.objects.get(name="Snake 12"),
        Snake.objects.get(name="Snake 15"),
    ]


@mock.patch("apps.game.models.Game.update_from_engine")
def test_bracket_with_25_snakes(update_mock):
    bracket = _arrange_tournament("single heat", 25)

    round1 = bracket.create_next_round()
    _complete_games_in_round(round1)
    round2 = bracket.create_next_round()
    _complete_games_in_round(round2)
    round3 = bracket.create_next_round()
    _complete_games_in_round(round3)
    round4 = bracket.create_next_round()
    _complete_games_in_round(round4)
    round5 = bracket.create_next_round()
    _complete_games_in_round(round5)

    assert round1.status == "complete"
    assert round2.status == "complete"
    assert round3.status == "complete"
    assert len(bracket.winners) == 3
    assert bracket.winners == [
        Snake.objects.get(name="Snake 1"),
        Snake.objects.get(name="Snake 10"),
        Snake.objects.get(name="Snake 11"),
    ]
    assert bracket.runner_ups == [
        Snake.objects.get(name="Snake 12"),
        Snake.objects.get(name="Snake 13"),
        Snake.objects.get(name="Snake 14"),
    ]


@mock.patch("apps.game.models.Game.update_from_engine")
def test_bracket_with_96_snakes(update_mock):
    bracket = _arrange_tournament("single heat", 96)

    round1 = bracket.create_next_round()
    _complete_games_in_round(round1)
    round2 = bracket.create_next_round()
    _complete_games_in_round(round2)
    round3 = bracket.create_next_round()
    _complete_games_in_round(round3)
    round4 = bracket.create_next_round()
    _complete_games_in_round(round4)
    round5 = bracket.create_next_round()
    _complete_games_in_round(round5)

    assert round1.status == "complete"
    assert round2.status == "complete"
    assert round3.status == "complete"
    assert len(bracket.winners) == 3
    assert bracket.winners == [
        Snake.objects.get(name="Snake 1"),
        Snake.objects.get(name="Snake 10"),
        Snake.objects.get(name="Snake 11"),
    ]
    assert bracket.runner_ups == [
        Snake.objects.get(name="Snake 12"),
        Snake.objects.get(name="Snake 13"),
        Snake.objects.get(name="Snake 14"),
    ]


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
    round5 = bracket.create_next_round()
    _complete_games_in_round(round5)
    round6 = bracket.create_next_round()
    _complete_games_in_round(round6)

    assert round1.status == "complete"
    assert round2.status == "complete"
    assert round3.status == "complete"
    assert round4.status == "complete"
    assert len(bracket.winners) == 3
    assert bracket.winners == [
        Snake.objects.get(name="Snake 1"),
        Snake.objects.get(name="Snake 10"),
        Snake.objects.get(name="Snake 11"),
    ]
    assert bracket.runner_ups == [
        Snake.objects.get(name="Snake 16"),
        Snake.objects.get(name="Snake 12"),
        Snake.objects.get(name="Snake 14"),
    ]
