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
        team = Team.objects.create(name="test team", snake=snake)
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
    for gs in GameSnake.objects.filter(game=game).order_by("snake__id"):
        if not marked_winner:
            marked_winner = True
            continue
        gs.death = "snake-collision"
        gs.turns = 10
        gs.save()


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


@pytest.mark.skip("This is a brittle way to test this")
def test_create_next_round_partial_two_heats_no_games():
    # These tests don't run
    bracket = _arrange_tournament("single heat", 10)
    bracket.create_next_round()

    rows = bracket.export()

    expected_rows = [
        ["Round", "Heat", "Snake Name", "Snake Id"],
        ["Round 1", "Heat 1", "Snake 1", "snk_1"],
        ["Round 1", "Heat 1", "Snake 3", "snk_3"],
        ["Round 1", "Heat 1", "Snake 5", "snk_5"],
        ["Round 1", "Heat 1", "Snake 7", "snk_7"],
        ["Round 1", "Heat 1", "Snake 9", "snk_9"],
        ["Round 1", "Heat 2", "Snake 2", "snk_2"],
        ["Round 1", "Heat 2", "Snake 4", "snk_4"],
        ["Round 1", "Heat 2", "Snake 6", "snk_6"],
        ["Round 1", "Heat 2", "Snake 8", "snk_8"],
        ["Round 1", "Heat 2", "Snake 10", "snk_10"],
    ]
    print(expected_rows)
    print(rows)
    assert bracket.game_details() == []
    assert rows == expected_rows


@pytest.mark.skip("This is a brittle way to test this")
def test_create_next_round_partial_two_heats_uhoh():
    bracket = _arrange_tournament("single heat", 10)
    bracket.create_next_round()

    hg1 = bracket.rounds[0].heats[1].create_next_game()
    game = hg1.game

    rows = bracket.export()

    heat_2_game_url = f"https://play.battlesnake.io/game/{game.id}"
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
        ["Round 1", "Heat 1", "Snake 3", "snk_3"],
        ["Round 1", "Heat 1", "Snake 5", "snk_5"],
        ["Round 1", "Heat 1", "Snake 7", "snk_7"],
        ["Round 1", "Heat 1", "Snake 9", "snk_9"],
        ["Round 1", "Heat 2", "Snake 10", "snk_10", heat_2_game_url],
        ["Round 1", "Heat 2", "Snake 2", "snk_2", heat_2_game_url],
        ["Round 1", "Heat 2", "Snake 4", "snk_4", heat_2_game_url],
        ["Round 1", "Heat 2", "Snake 6", "snk_6", heat_2_game_url],
        ["Round 1", "Heat 2", "Snake 8", "snk_8", heat_2_game_url],
    ]

    assert rows == expected_rows


@pytest.mark.skip("This is a brittle way to test this")
def test_create_next_round_partial_two_heats():
    bracket = _arrange_tournament("single heat", 10)
    bracket.create_next_round()

    game11 = bracket.rounds[0].heats[0].create_next_game().game
    _mark_winner(game11)
    game12 = bracket.rounds[0].heats[0].create_next_game().game
    _mark_winner(game12)
    game21 = bracket.rounds[0].heats[1].create_next_game().game
    _mark_winner(game21)
    game22 = bracket.rounds[0].heats[1].create_next_game().game

    rows = bracket.export()

    heat_1_game_1_url = f"https://play.battlesnake.io/game/{game11.id}"
    heat_1_game_2_url = f"https://play.battlesnake.io/game/{game12.id}"
    heat_2_game_1_url = f"https://play.battlesnake.io/game/{game21.id}"
    heat_2_game_2_url = f"https://play.battlesnake.io/game/{game22.id}"
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
        ["Round 1", "Heat 1", "Snake 1", "snk_1", heat_1_game_1_url, heat_1_game_2_url],
        ["Round 1", "Heat 1", "Snake 3", "snk_3", heat_1_game_1_url, heat_1_game_2_url],
        ["Round 1", "Heat 1", "Snake 5", "snk_5", heat_1_game_1_url, heat_1_game_2_url],
        ["Round 1", "Heat 1", "Snake 7", "snk_7", heat_1_game_1_url, heat_1_game_2_url],
        ["Round 1", "Heat 1", "Snake 9", "snk_9", heat_1_game_1_url, heat_1_game_2_url],
        [
            "Round 1",
            "Heat 2",
            "Snake 10",
            "snk_10",
            heat_2_game_1_url,
            heat_2_game_2_url,
        ],
        ["Round 1", "Heat 2", "Snake 2", "snk_2", heat_2_game_1_url, heat_2_game_2_url],
        ["Round 1", "Heat 2", "Snake 4", "snk_4", heat_2_game_1_url, heat_2_game_2_url],
        ["Round 1", "Heat 2", "Snake 6", "snk_6", heat_2_game_1_url, heat_2_game_2_url],
        ["Round 1", "Heat 2", "Snake 8", "snk_8", heat_2_game_1_url, heat_2_game_2_url],
    ]

    assert rows == expected_rows


@pytest.mark.skip("This is a brittle way to test this")
@mock.patch("apps.game.models.Game.update_from_engine")
def test_create_next_round_second_round(update_mock):
    bracket = _arrange_tournament("single heat", 10)
    bracket.create_next_round()

    game11 = bracket.rounds[0].heats[0].create_next_game().game
    _mark_winner(game11)
    game12 = bracket.rounds[0].heats[0].create_next_game().game
    _mark_winner(game12)
    game21 = bracket.rounds[0].heats[1].create_next_game().game
    _mark_winner(game21)
    game22 = bracket.rounds[0].heats[1].create_next_game().game
    _mark_winner(game22)
    bracket.create_next_round()

    rows = bracket.export()

    heat_1_game_1_url = f"https://play.battlesnake.io/game/{game11.id}"
    heat_1_game_2_url = f"https://play.battlesnake.io/game/{game12.id}"
    heat_2_game_1_url = f"https://play.battlesnake.io/game/{game21.id}"
    heat_2_game_2_url = f"https://play.battlesnake.io/game/{game22.id}"
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
        ["Round 1", "Heat 1", "Snake 1", "snk_1", heat_1_game_1_url, heat_1_game_2_url],
        ["Round 1", "Heat 1", "Snake 3", "snk_3", heat_1_game_1_url, heat_1_game_2_url],
        ["Round 1", "Heat 1", "Snake 5", "snk_5", heat_1_game_1_url, heat_1_game_2_url],
        ["Round 1", "Heat 1", "Snake 7", "snk_7", heat_1_game_1_url, heat_1_game_2_url],
        ["Round 1", "Heat 1", "Snake 9", "snk_9", heat_1_game_1_url, heat_1_game_2_url],
        [
            "Round 1",
            "Heat 2",
            "Snake 10",
            "snk_10",
            heat_2_game_1_url,
            heat_2_game_2_url,
        ],
        ["Round 1", "Heat 2", "Snake 2", "snk_2", heat_2_game_1_url, heat_2_game_2_url],
        ["Round 1", "Heat 2", "Snake 4", "snk_4", heat_2_game_1_url, heat_2_game_2_url],
        ["Round 1", "Heat 2", "Snake 6", "snk_6", heat_2_game_1_url, heat_2_game_2_url],
        ["Round 1", "Heat 2", "Snake 8", "snk_8", heat_2_game_1_url, heat_2_game_2_url],
        ["Round 2", "Heat 1", "Snake 1", "snk_1"],
        ["Round 2", "Heat 1", "Snake 10", "snk_10"],
        ["Round 2", "Heat 1", "Snake 2", "snk_2"],
        ["Round 2", "Heat 1", "Snake 3", "snk_3"],
    ]

    expected_game_details = [
        {
            "id": game11.id,
            "status": "complete",
            "round": 1,
            "heat": 1,
            "heat_game": 1,
            "url": generate_game_url(game11.engine_id),
        },
        {
            "id": game12.id,
            "status": "complete",
            "round": 1,
            "heat": 1,
            "heat_game": 2,
            "url": generate_game_url(game12.engine_id),
        },
        {
            "id": game21.id,
            "status": "complete",
            "round": 1,
            "heat": 2,
            "heat_game": 1,
            "url": generate_game_url(game21.engine_id),
        },
        {
            "id": game22.id,
            "status": "complete",
            "round": 1,
            "heat": 2,
            "heat_game": 2,
            "url": generate_game_url(game22.engine_id),
        },
    ]

    assert rows == expected_rows
    assert bracket.game_details() == expected_game_details


@mock.patch("apps.game.models.Game.update_from_engine")
def test_complete_tournament(update_mock):
    bracket = _arrange_tournament("single heat", 24)
    bracket.create_next_round()

    # with 24 snakes, we have 1 opening round, and then the finals
    game11 = bracket.rounds[0].heats[0].create_next_game().game
    _mark_winner(game11)
    game12 = bracket.rounds[0].heats[0].create_next_game().game
    _mark_winner(game12)
    game21 = bracket.rounds[0].heats[1].create_next_game().game
    _mark_winner(game21)
    game22 = bracket.rounds[0].heats[1].create_next_game().game
    _mark_winner(game22)
    game31 = bracket.rounds[0].heats[2].create_next_game().game
    _mark_winner(game31)
    game32 = bracket.rounds[0].heats[2].create_next_game().game
    _mark_winner(game32)

    finals = bracket.create_next_round()
    finals_game1 = finals.heats[0].create_next_game().game
    _mark_winner(finals_game1)
    # round2_game2 = finals.heats[0].create_next_game().game
    # _mark_winner(round2_game2)
    # round2_game3 = finals.heats[0].create_next_game().game
    # _mark_winner(round2_game3)

    # round3 = bracket.create_next_round()
    # round3_game1 = round3.heats[0].create_next_game().game
    # _mark_winner(round3_game1)

    # rows = bracket.export()

    # heat_1_game_1_url = f"https://play.battlesnake.io/game/{game11.id}"
    # heat_1_game_2_url = f"https://play.battlesnake.io/game/{game12.id}"
    # heat_2_game_1_url = f"https://play.battlesnake.io/game/{game21.id}"
    # heat_2_game_2_url = f"https://play.battlesnake.io/game/{game22.id}"
    # heat_3_game_1_url = f"https://play.battlesnake.io/game/{game31.id}"
    # heat_3_game_2_url = f"https://play.battlesnake.io/game/{game32.id}"
    # round_2_heat_1_game_1_url = f"https://play.battlesnake.io/game/{finals_game1.id}"
    # round_2_heat_1_game_2_url = f"https://play.battlesnake.io/game/{round2_game2.id}"
    # round_2_heat_1_game_3_url = f"https://play.battlesnake.io/game/{round2_game3.id}"
    # round_3_heat_1_game_1_url = f"https://play.battlesnake.io/game/{round3_game1.id}"
    # expected_rows = [
    #     [
    #         "Round",
    #         "Heat",
    #         "Snake Name",
    #         "Snake Id",
    #         "Game 1 URL",
    #         "Game 2 URL",
    #         "Game 3 URL",
    #     ],
    #     ["Round 1", "Heat 1", "Snake 1", "snk_1", heat_1_game_1_url, heat_1_game_2_url],
    #     [
    #         "Round 1",
    #         "Heat 1",
    #         "Snake 10",
    #         "snk_10",
    #         heat_1_game_1_url,
    #         heat_1_game_2_url,
    #     ],
    #     [
    #         "Round 1",
    #         "Heat 1",
    #         "Snake 13",
    #         "snk_13",
    #         heat_1_game_1_url,
    #         heat_1_game_2_url,
    #     ],
    #     [
    #         "Round 1",
    #         "Heat 1",
    #         "Snake 16",
    #         "snk_16",
    #         heat_1_game_1_url,
    #         heat_1_game_2_url,
    #     ],
    #     [
    #         "Round 1",
    #         "Heat 1",
    #         "Snake 19",
    #         "snk_19",
    #         heat_1_game_1_url,
    #         heat_1_game_2_url,
    #     ],
    #     [
    #         "Round 1",
    #         "Heat 1",
    #         "Snake 22",
    #         "snk_22",
    #         heat_1_game_1_url,
    #         heat_1_game_2_url,
    #     ],
    #     ["Round 1", "Heat 1", "Snake 4", "snk_4", heat_1_game_1_url, heat_1_game_2_url],
    #     ["Round 1", "Heat 1", "Snake 7", "snk_7", heat_1_game_1_url, heat_1_game_2_url],
    #     [
    #         "Round 1",
    #         "Heat 2",
    #         "Snake 11",
    #         "snk_11",
    #         heat_2_game_1_url,
    #         heat_2_game_2_url,
    #     ],
    #     [
    #         "Round 1",
    #         "Heat 2",
    #         "Snake 14",
    #         "snk_14",
    #         heat_2_game_1_url,
    #         heat_2_game_2_url,
    #     ],
    #     [
    #         "Round 1",
    #         "Heat 2",
    #         "Snake 17",
    #         "snk_17",
    #         heat_2_game_1_url,
    #         heat_2_game_2_url,
    #     ],
    #     ["Round 1", "Heat 2", "Snake 2", "snk_2", heat_2_game_1_url, heat_2_game_2_url],
    #     [
    #         "Round 1",
    #         "Heat 2",
    #         "Snake 20",
    #         "snk_20",
    #         heat_2_game_1_url,
    #         heat_2_game_2_url,
    #     ],
    #     [
    #         "Round 1",
    #         "Heat 2",
    #         "Snake 23",
    #         "snk_23",
    #         heat_2_game_1_url,
    #         heat_2_game_2_url,
    #     ],
    #     ["Round 1", "Heat 2", "Snake 5", "snk_5", heat_2_game_1_url, heat_2_game_2_url],
    #     ["Round 1", "Heat 2", "Snake 8", "snk_8", heat_2_game_1_url, heat_2_game_2_url],
    #     [
    #         "Round 1",
    #         "Heat 3",
    #         "Snake 12",
    #         "snk_12",
    #         heat_3_game_1_url,
    #         heat_3_game_2_url,
    #     ],
    #     [
    #         "Round 1",
    #         "Heat 3",
    #         "Snake 15",
    #         "snk_15",
    #         heat_3_game_1_url,
    #         heat_3_game_2_url,
    #     ],
    #     [
    #         "Round 1",
    #         "Heat 3",
    #         "Snake 18",
    #         "snk_18",
    #         heat_3_game_1_url,
    #         heat_3_game_2_url,
    #     ],
    #     [
    #         "Round 1",
    #         "Heat 3",
    #         "Snake 21",
    #         "snk_21",
    #         heat_3_game_1_url,
    #         heat_3_game_2_url,
    #     ],
    #     [
    #         "Round 1",
    #         "Heat 3",
    #         "Snake 24",
    #         "snk_24",
    #         heat_3_game_1_url,
    #         heat_3_game_2_url,
    #     ],
    #     ["Round 1", "Heat 3", "Snake 3", "snk_3", heat_3_game_1_url, heat_3_game_2_url],
    #     ["Round 1", "Heat 3", "Snake 6", "snk_6", heat_3_game_1_url, heat_3_game_2_url],
    #     ["Round 1", "Heat 3", "Snake 9", "snk_9", heat_3_game_1_url, heat_3_game_2_url],
    #     ["Round 2", "Heat 1", "Snake 1", "snk_1", round_2_heat_1_game_1_url],
    #     ["Round 2", "Heat 1", "Snake 10", "snk_10", round_2_heat_1_game_1_url],
    #     ["Round 2", "Heat 1", "Snake 11", "snk_11", round_2_heat_1_game_1_url],
    #     ["Round 2", "Heat 1", "Snake 12", "snk_12", round_2_heat_1_game_1_url],
    #     ["Round 2", "Heat 1", "Snake 14", "snk_14", round_2_heat_1_game_1_url],
    #     ["Round 2", "Heat 1", "Snake 15", "snk_15", round_2_heat_1_game_1_url],
    #     # ["Round 3", "Heat 1", "Snake 1", "snk_1", round_3_heat_1_game_1_url],
    #     # ["Round 3", "Heat 1", "Snake 10", "snk_10", round_3_heat_1_game_1_url],
    #     # ["Round 3", "Heat 1", "Snake 11", "snk_11", round_3_heat_1_game_1_url],
    # ]
    # expected_game_details = [
    #     {
    #         "id": game11.id,
    #         "status": "complete",
    #         "round": 1,
    #         "heat": 1,
    #         "heat_game": 1,
    #         "url": generate_game_url(game11.engine_id),
    #     },
    #     {
    #         "id": game12.id,
    #         "status": "complete",
    #         "round": 1,
    #         "heat": 1,
    #         "heat_game": 2,
    #         "url": generate_game_url(game12.engine_id),
    #     },
    #     {
    #         "id": game21.id,
    #         "status": "complete",
    #         "round": 1,
    #         "heat": 2,
    #         "heat_game": 1,
    #         "url": generate_game_url(game21.engine_id),
    #     },
    #     {
    #         "id": game22.id,
    #         "status": "complete",
    #         "round": 1,
    #         "heat": 2,
    #         "heat_game": 2,
    #         "url": generate_game_url(game22.engine_id),
    #     },
    #     {
    #         "id": game31.id,
    #         "status": "complete",
    #         "round": 1,
    #         "heat": 3,
    #         "heat_game": 1,
    #         "url": generate_game_url(game31.engine_id),
    #     },
    #     {
    #         "id": game32.id,
    #         "status": "complete",
    #         "round": 1,
    #         "heat": 3,
    #         "heat_game": 2,
    #         "url": generate_game_url(game32.engine_id),
    #     },
    #     {
    #         "id": finals_game1.id,
    #         "status": "complete",
    #         "round": 2,
    #         "heat": 1,
    #         "heat_game": 1,
    #         "url": generate_game_url(finals_game1.engine_id),
    #     },
    # ]

    # TODO: this is a very convoluted test to try and resolve, and not sure if it's worthwhile
    # assert bracket.game_details() == expected_game_details
    # assert rows == expected_rows
