from apps.tournament.models import Tournament, SnakeTournament, Snake


def _arrange_tournament(name, num_snakes=8):
    t = Tournament.objects.create(name=name)
    snakes = []
    for i in range(1, num_snakes+1):
        snake = Snake.objects.create(
            name="Snake {}".format(i),
            id="snk_{}".format(i)
        )
        snakes.append(snake)
        SnakeTournament.objects.create(
            snake=snake,
            tournament=t,
        )
    return t


def test_build_structure_partial_single_heat():
    t = _arrange_tournament("single heat", 5)
    t.build_structure()

    rows = t.get_csv()

    expected_rows = [
        ['Round', 'Heat', 'Snake Name', 'Snake Id', "Game 1 URL", "Game 2 URL"],
        ['Round 1', 'Heat 1', 'Snake 1', 'snk_1'],
        ['Round 1', 'Heat 1', 'Snake 2', 'snk_2'],
        ['Round 1', 'Heat 1', 'Snake 3', 'snk_3'],
        ['Round 1', 'Heat 1', 'Snake 4', 'snk_4'],
        ['Round 1', 'Heat 1', 'Snake 5', 'snk_5'],
    ]
    assert rows == expected_rows


def test_build_structure_partial_two_heats():
    t = _arrange_tournament("single heat", 10)
    t.build_structure()

    rows = t.get_csv()

    expected_rows = [
        ['Round', 'Heat', 'Snake Name', 'Snake Id'],
        ['Round 1', 'Heat 1', 'Snake 1', 'snk_1'],
        ['Round 1', 'Heat 1', 'Snake 3', 'snk_3'],
        ['Round 1', 'Heat 1', 'Snake 5', 'snk_5'],
        ['Round 1', 'Heat 1', 'Snake 7', 'snk_7'],
        ['Round 1', 'Heat 1', 'Snake 9', 'snk_9'],
        ['Round 1', 'Heat 2', 'Snake 2', 'snk_2'],
        ['Round 1', 'Heat 2', 'Snake 4', 'snk_4'],
        ['Round 1', 'Heat 2', 'Snake 6', 'snk_6'],
        ['Round 1', 'Heat 2', 'Snake 8', 'snk_8'],
        ['Round 1', 'Heat 2', 'Snake 10', 'snk_10'],
    ]
    assert rows == expected_rows


def test_build_structure_partial_two_heats():
    t = _arrange_tournament("single heat", 10)
    t.build_structure()

    hg1 = t.rounds[0].heats[1].create_next_game()
    game = hg1.game

    rows = t.get_csv()

    heat_2_game_url = "https://play.battlesnake.io/game/{}".format(game.id)
    expected_rows = [
        ['Round', 'Heat', 'Snake Name', 'Snake Id', "Game 1 URL", "Game 2 URL"],
        ['Round 1', 'Heat 1', 'Snake 1', 'snk_1'],
        ['Round 1', 'Heat 1', 'Snake 3', 'snk_3'],
        ['Round 1', 'Heat 1', 'Snake 5', 'snk_5'],
        ['Round 1', 'Heat 1', 'Snake 7', 'snk_7'],
        ['Round 1', 'Heat 1', 'Snake 9', 'snk_9'],
        ['Round 1', 'Heat 2', 'Snake 2', 'snk_2', heat_2_game_url],
        ['Round 1', 'Heat 2', 'Snake 4', 'snk_4', heat_2_game_url],
        ['Round 1', 'Heat 2', 'Snake 6', 'snk_6', heat_2_game_url],
        ['Round 1', 'Heat 2', 'Snake 8', 'snk_8', heat_2_game_url],
        ['Round 1', 'Heat 2', 'Snake 10', 'snk_10', heat_2_game_url],
    ]

    assert rows == expected_rows


def test_build_structure_partial_two_heats():
    t = _arrange_tournament("single heat", 10)
    t.build_structure()

    game11 = t.rounds[0].heats[0].create_next_game().game
    game12 = t.rounds[0].heats[0].create_next_game().game
    game21 = t.rounds[0].heats[1].create_next_game().game
    game22 = t.rounds[0].heats[1].create_next_game().game

    rows = t.get_csv()

    heat_1_game_1_url = "https://play.battlesnake.io/game/{}".format(game11.id)
    heat_1_game_2_url = "https://play.battlesnake.io/game/{}".format(game12.id)
    heat_2_game_1_url = "https://play.battlesnake.io/game/{}".format(game21.id)
    heat_2_game_2_url = "https://play.battlesnake.io/game/{}".format(game22.id)
    expected_rows = [
        ['Round', 'Heat', 'Snake Name', 'Snake Id', "Game 1 URL", "Game 2 URL"],
        ['Round 1', 'Heat 1', 'Snake 1', 'snk_1', heat_1_game_1_url, heat_1_game_2_url],
        ['Round 1', 'Heat 1', 'Snake 3', 'snk_3', heat_1_game_1_url, heat_1_game_2_url],
        ['Round 1', 'Heat 1', 'Snake 5', 'snk_5', heat_1_game_1_url, heat_1_game_2_url],
        ['Round 1', 'Heat 1', 'Snake 7', 'snk_7', heat_1_game_1_url, heat_1_game_2_url],
        ['Round 1', 'Heat 1', 'Snake 9', 'snk_9', heat_1_game_1_url, heat_1_game_2_url],
        ['Round 1', 'Heat 2', 'Snake 2', 'snk_2', heat_2_game_1_url, heat_2_game_2_url],
        ['Round 1', 'Heat 2', 'Snake 4', 'snk_4', heat_2_game_1_url, heat_2_game_2_url],
        ['Round 1', 'Heat 2', 'Snake 6', 'snk_6', heat_2_game_1_url, heat_2_game_2_url],
        ['Round 1', 'Heat 2', 'Snake 8', 'snk_8', heat_2_game_1_url, heat_2_game_2_url],
        ['Round 1', 'Heat 2', 'Snake 10', 'snk_10', heat_2_game_1_url, heat_2_game_2_url],
    ]

    assert rows == expected_rows


def test_build_structure_second_round():
    t = _arrange_tournament("single heat", 10)
    t.build_structure()

    game11 = t.rounds[0].heats[0].create_next_game().game
    game12 = t.rounds[0].heats[0].create_next_game().game
    game21 = t.rounds[0].heats[1].create_next_game().game
    game22 = t.rounds[0].heats[1].create_next_game().game

    rows = t.get_csv()

    heat_1_game_1_url = "https://play.battlesnake.io/game/{}".format(game11.id)
    heat_1_game_2_url = "https://play.battlesnake.io/game/{}".format(game12.id)
    heat_2_game_1_url = "https://play.battlesnake.io/game/{}".format(game21.id)
    heat_2_game_2_url = "https://play.battlesnake.io/game/{}".format(game22.id)
    expected_rows = [
        ['Round', 'Heat', 'Snake Name', 'Snake Id', "Game 1 URL", "Game 2 URL"],
        ['Round 1', 'Heat 1', 'Snake 1', 'snk_1', heat_1_game_1_url, heat_1_game_2_url],
        ['Round 1', 'Heat 1', 'Snake 3', 'snk_3', heat_1_game_1_url, heat_1_game_2_url],
        ['Round 1', 'Heat 1', 'Snake 5', 'snk_5', heat_1_game_1_url, heat_1_game_2_url],
        ['Round 1', 'Heat 1', 'Snake 7', 'snk_7', heat_1_game_1_url, heat_1_game_2_url],
        ['Round 1', 'Heat 1', 'Snake 9', 'snk_9', heat_1_game_1_url, heat_1_game_2_url],
        ['Round 1', 'Heat 2', 'Snake 2', 'snk_2', heat_2_game_1_url, heat_2_game_2_url],
        ['Round 1', 'Heat 2', 'Snake 4', 'snk_4', heat_2_game_1_url, heat_2_game_2_url],
        ['Round 1', 'Heat 2', 'Snake 6', 'snk_6', heat_2_game_1_url, heat_2_game_2_url],
        ['Round 1', 'Heat 2', 'Snake 8', 'snk_8', heat_2_game_1_url, heat_2_game_2_url],
        ['Round 1', 'Heat 2', 'Snake 10', 'snk_10', heat_2_game_1_url, heat_2_game_2_url],
    ]

    assert rows == expected_rows
