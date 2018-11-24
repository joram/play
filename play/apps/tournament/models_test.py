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


def _mark_winner(game):
    game.status = game.Status.COMPLETE
    game.save()
    from apps.game.models import GameSnake
    marked_winner = False
    for gs in GameSnake.objects.filter(game=game):
        if not marked_winner:
            marked_winner = True
            continue
        gs.death = "snake-collision"
        gs.turns = 10
        gs.save()


def test_create_next_round_partial_single_heat():
    t = _arrange_tournament("single heat", 5)
    t.create_next_round()

    rows = t.export()

    expected_rows = [
        ['Round', 'Heat', 'Snake Name', 'Snake Id', "Game 1 URL", "Game 2 URL", "Game 3 URL"],
        ['Round 1', 'Heat 1', 'Snake 1', 'snk_1'],
        ['Round 1', 'Heat 1', 'Snake 2', 'snk_2'],
        ['Round 1', 'Heat 1', 'Snake 3', 'snk_3'],
        ['Round 1', 'Heat 1', 'Snake 4', 'snk_4'],
        ['Round 1', 'Heat 1', 'Snake 5', 'snk_5'],
    ]

    assert rows == expected_rows


def test_create_next_round_partial_two_heats():
    t = _arrange_tournament("single heat", 10)
    t.create_next_round()

    rows = t.export()

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


def test_create_next_round_partial_two_heats():
    t = _arrange_tournament("single heat", 10)
    t.create_next_round()

    hg1 = t.rounds[0].heats[1].create_next_game()
    game = hg1.game

    rows = t.export()

    heat_2_game_url = "https://play.battlesnake.io/game/{}".format(game.id)
    expected_rows = [
        ['Round', 'Heat', 'Snake Name', 'Snake Id', "Game 1 URL", "Game 2 URL", "Game 3 URL"],
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


def test_create_next_round_partial_two_heats():
    t = _arrange_tournament("single heat", 10)
    t.create_next_round()

    game11 = t.rounds[0].heats[0].create_next_game().game
    _mark_winner(game11)
    game12 = t.rounds[0].heats[0].create_next_game().game
    game21 = t.rounds[0].heats[1].create_next_game().game
    _mark_winner(game21)
    game22 = t.rounds[0].heats[1].create_next_game().game

    rows = t.export()

    heat_1_game_1_url = "https://play.battlesnake.io/game/{}".format(game11.id)
    heat_1_game_2_url = "https://play.battlesnake.io/game/{}".format(game12.id)
    heat_2_game_1_url = "https://play.battlesnake.io/game/{}".format(game21.id)
    heat_2_game_2_url = "https://play.battlesnake.io/game/{}".format(game22.id)
    expected_rows = [
        ['Round', 'Heat', 'Snake Name', 'Snake Id', "Game 1 URL", "Game 2 URL", "Game 3 URL"],
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


def test_create_next_round_second_round():
    t = _arrange_tournament("single heat", 10)
    t.create_next_round()

    game11 = t.rounds[0].heats[0].create_next_game().game
    _mark_winner(game11)
    game12 = t.rounds[0].heats[0].create_next_game().game
    _mark_winner(game12)
    game21 = t.rounds[0].heats[1].create_next_game().game
    _mark_winner(game21)
    game22 = t.rounds[0].heats[1].create_next_game().game
    _mark_winner(game22)
    t.create_next_round()

    rows = t.export()

    heat_1_game_1_url = "https://play.battlesnake.io/game/{}".format(game11.id)
    heat_1_game_2_url = "https://play.battlesnake.io/game/{}".format(game12.id)
    heat_2_game_1_url = "https://play.battlesnake.io/game/{}".format(game21.id)
    heat_2_game_2_url = "https://play.battlesnake.io/game/{}".format(game22.id)
    expected_rows = [
        ['Round', 'Heat', 'Snake Name', 'Snake Id', "Game 1 URL", "Game 2 URL", "Game 3 URL"],
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
        ['Round 2', 'Heat 1', 'Snake 1', 'snk_1'],
        ['Round 2', 'Heat 1', 'Snake 2', 'snk_2'],
        ['Round 2', 'Heat 1', 'Snake 3', 'snk_3'],
        ['Round 2', 'Heat 1', 'Snake 4', 'snk_4'],
    ]

    assert rows == expected_rows


def test_complete_tournament():
    t = _arrange_tournament("single heat", 24)
    t.create_next_round()

    game11 = t.rounds[0].heats[0].create_next_game().game
    _mark_winner(game11)
    game12 = t.rounds[0].heats[0].create_next_game().game
    _mark_winner(game12)
    game21 = t.rounds[0].heats[1].create_next_game().game
    _mark_winner(game21)
    game22 = t.rounds[0].heats[1].create_next_game().game
    _mark_winner(game22)
    game31 = t.rounds[0].heats[2].create_next_game().game
    _mark_winner(game31)
    game32 = t.rounds[0].heats[2].create_next_game().game
    _mark_winner(game32)

    round2 = t.create_next_round()
    round2_game1 = round2.heats[0].create_next_game().game
    _mark_winner(round2_game1)
    round2_game2 = round2.heats[0].create_next_game().game
    _mark_winner(round2_game2)
    round2_game3 = round2.heats[0].create_next_game().game
    _mark_winner(round2_game3)

    round3 = t.create_next_round()
    round3_game1 = round3.heats[0].create_next_game().game
    _mark_winner(round3_game1)

    rows = t.export()

    heat_1_game_1_url = "https://play.battlesnake.io/game/{}".format(game11.id)
    heat_1_game_2_url = "https://play.battlesnake.io/game/{}".format(game12.id)
    heat_2_game_1_url = "https://play.battlesnake.io/game/{}".format(game21.id)
    heat_2_game_2_url = "https://play.battlesnake.io/game/{}".format(game22.id)
    heat_3_game_1_url = "https://play.battlesnake.io/game/{}".format(game31.id)
    heat_3_game_2_url = "https://play.battlesnake.io/game/{}".format(game32.id)
    round_2_heat_1_game_1_url = "https://play.battlesnake.io/game/{}".format(round2_game1.id)
    round_2_heat_1_game_2_url = "https://play.battlesnake.io/game/{}".format(round2_game2.id)
    round_2_heat_1_game_3_url = "https://play.battlesnake.io/game/{}".format(round2_game3.id)
    round_3_heat_1_game_1_url = "https://play.battlesnake.io/game/{}".format(round3_game1.id)
    expected_rows = [
        ['Round', 'Heat', 'Snake Name', 'Snake Id', "Game 1 URL", "Game 2 URL", "Game 3 URL"],
        
        ['Round 1', 'Heat 1', 'Snake 1', 'snk_1', heat_1_game_1_url, heat_1_game_2_url],
        ['Round 1', 'Heat 1', 'Snake 4', 'snk_4', heat_1_game_1_url, heat_1_game_2_url],
        ['Round 1', 'Heat 1', 'Snake 7', 'snk_7', heat_1_game_1_url, heat_1_game_2_url],
        ['Round 1', 'Heat 1', 'Snake 10', 'snk_10', heat_1_game_1_url, heat_1_game_2_url],
        ['Round 1', 'Heat 1', 'Snake 13', 'snk_13', heat_1_game_1_url, heat_1_game_2_url],
        ['Round 1', 'Heat 1', 'Snake 16', 'snk_16', heat_1_game_1_url, heat_1_game_2_url],
        ['Round 1', 'Heat 1', 'Snake 19', 'snk_19', heat_1_game_1_url, heat_1_game_2_url],
        ['Round 1', 'Heat 1', 'Snake 22', 'snk_22', heat_1_game_1_url, heat_1_game_2_url],

        ['Round 1', 'Heat 2', 'Snake 2', 'snk_2', heat_2_game_1_url, heat_2_game_2_url],
        ['Round 1', 'Heat 2', 'Snake 5', 'snk_5', heat_2_game_1_url, heat_2_game_2_url],
        ['Round 1', 'Heat 2', 'Snake 8', 'snk_8', heat_2_game_1_url, heat_2_game_2_url],
        ['Round 1', 'Heat 2', 'Snake 11', 'snk_11', heat_2_game_1_url, heat_2_game_2_url],
        ['Round 1', 'Heat 2', 'Snake 14', 'snk_14', heat_2_game_1_url, heat_2_game_2_url],
        ['Round 1', 'Heat 2', 'Snake 17', 'snk_17', heat_2_game_1_url, heat_2_game_2_url],
        ['Round 1', 'Heat 2', 'Snake 20', 'snk_20', heat_2_game_1_url, heat_2_game_2_url],
        ['Round 1', 'Heat 2', 'Snake 23', 'snk_23', heat_2_game_1_url, heat_2_game_2_url],

        ['Round 1', 'Heat 3', 'Snake 3', 'snk_3', heat_3_game_1_url, heat_3_game_2_url],
        ['Round 1', 'Heat 3', 'Snake 6', 'snk_6', heat_3_game_1_url, heat_3_game_2_url],
        ['Round 1', 'Heat 3', 'Snake 9', 'snk_9', heat_3_game_1_url, heat_3_game_2_url],
        ['Round 1', 'Heat 3', 'Snake 12', 'snk_12', heat_3_game_1_url, heat_3_game_2_url],
        ['Round 1', 'Heat 3', 'Snake 15', 'snk_15', heat_3_game_1_url, heat_3_game_2_url],
        ['Round 1', 'Heat 3', 'Snake 18', 'snk_18', heat_3_game_1_url, heat_3_game_2_url],
        ['Round 1', 'Heat 3', 'Snake 21', 'snk_21', heat_3_game_1_url, heat_3_game_2_url],
        ['Round 1', 'Heat 3', 'Snake 24', 'snk_24', heat_3_game_1_url, heat_3_game_2_url],

        ['Round 2', 'Heat 1', 'Snake 1', 'snk_1', round_2_heat_1_game_1_url, round_2_heat_1_game_2_url, round_2_heat_1_game_3_url],
        ['Round 2', 'Heat 1', 'Snake 2', 'snk_2', round_2_heat_1_game_1_url, round_2_heat_1_game_2_url, round_2_heat_1_game_3_url],
        ['Round 2', 'Heat 1', 'Snake 3', 'snk_3', round_2_heat_1_game_1_url, round_2_heat_1_game_2_url, round_2_heat_1_game_3_url],
        ['Round 2', 'Heat 1', 'Snake 4', 'snk_4', round_2_heat_1_game_1_url, round_2_heat_1_game_2_url, round_2_heat_1_game_3_url],
        ['Round 2', 'Heat 1', 'Snake 5', 'snk_5', round_2_heat_1_game_1_url, round_2_heat_1_game_2_url, round_2_heat_1_game_3_url],
        ['Round 2', 'Heat 1', 'Snake 6', 'snk_6', round_2_heat_1_game_1_url, round_2_heat_1_game_2_url, round_2_heat_1_game_3_url],

        ['Round 3', 'Heat 1', 'Snake 1', 'snk_1', round_3_heat_1_game_1_url],
        ['Round 3', 'Heat 1', 'Snake 2', 'snk_2', round_3_heat_1_game_1_url],
        ['Round 3', 'Heat 1', 'Snake 3', 'snk_3', round_3_heat_1_game_1_url],
    ]

    import pprint
    pprint.pprint(rows)
    assert rows == expected_rows
