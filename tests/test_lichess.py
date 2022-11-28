import pytest

from services.lichess import (
    get_username_of,
    is_lose,
    played_for,
    get_short_opening_name,
    group_lost_games_by_opening,
)


@pytest.fixture
def game_example_data():
    return {
      "clock": {
        "increment": 2,
        "initial": 180,
        "totalTime": 260
      },
      "createdAt": "Mon, 28 Nov 2022 05:29:46 GMT",
      "id": "8Ybm4Xh4",
      "lastMoveAt": "Mon, 28 Nov 2022 05:37:25 GMT",
      "moves": "e4 a5 Bc4 d6 Qf3 Nf6 d4 Nbd7 a3 h6 Nh3 c6 e5 dxe5 dxe5 Nxe5 Qf4 Nxc4 Qxc4 Bxh3 gxh3 e6 Nc3 Bd6 Bd2 O-O O-O-O Rc8 Rhg1 b5 Qd4 e5 Qd3 Re8 Bxh6 g6 Qf3 b4 Ne4 Nxe4 Qxe4 Qf6 h4 c5 h5 Re6 hxg6 fxg6 h4 Bf8 Bg5 Qf5 Qxf5 gxf5 Rd7 Rg6 h5 Rxg5 Rxg5+ Kh8 h6 Bxh6 f4 Bxg5 fxg5 c4 g6 Rg8 Rh7#",
      "opening": {
        "eco": "B00",
        "name": "Ware Defense",
        "ply": 2
      },
      "perf": "blitz",
      "players": {
        "black": {
          "rating": 1432,
          "ratingDiff": -7,
          "user": {
            "id": "ilyasgaripov",
            "name": "ilyasgaripov"
          }
        },
        "white": {
          "rating": 1404,
          "ratingDiff": 6,
          "user": {
            "id": "thetiger1988",
            "name": "TheTiger1988"
          }
        }
      },
      "rated": True,
      "speed": "blitz",
      "status": "mate",
      "variant": "standard",
      "winner": "white"
   }


@pytest.fixture()
def get_example_games():
    return [
        {
            'id': 'wvV0xviw',
            'players': {
                'white': {'user': {'name': 'player'}},
                'black': {'user': {'name': 'enemy'}},
            },
            'winner': 'black',
            'opening': {'name': "Queen's Pawn Game: Anti-Torre"},
        },
        {
            'id': 'YcY8XFMM',
            'players': {
                'white': {'user': {'name': 'enemy'}},
                'black': {'user': {'name': 'player'}},
            },
            'winner': 'white',
            'opening': {'name': "Queen's Pawn Game: Accelerated London System"},
        },
        {
            'id': 'DcD9XaMM',
            'players': {
                'white': {'user': {'name': 'player'}},
                'black': {'user': {'name': 'enemy'}},
            },
            'winner': 'black',
            'opening': {'name': "Zukertort Opening: Black Mustang Defense"},
        },
        {
            'id': '8Z2AcS1F',
            'players': {
                'white': {'user': {'name': 'player'}},
                'black': {'user': {'name': 'enemy'}},
            },
            'winner': 'white',
            'opening': {'name': "Queen's Pawn Game: Chigorin Variation"}
        }
    ]


def test_get_username_of():
    players = {
        'white': {'user': {'name': 'player_username'}},
        'black': {'user': {'name': 'enemy_username'}},
    }
    assert get_username_of(players, 'white') == 'player_username'
    assert get_username_of(players, 'black') == 'enemy_username'


def test_is_lose(game_example_data):
    assert is_lose(game_example_data, 'ilyasgaripov') == True
    assert is_lose(game_example_data, 'thetiger1988') == False


def test_played_for_white_side():
    players = {
        'white': {'user': {'name': 'player_username'}},
        'black': {'user': {'name': 'enemy_username'}},
    }
    username = 'player_username'
    assert played_for(players, username) == 'white'


def test_played_for_black_side():
    players = {
        'white': {'user': {'name': 'enemy_username'}},
        'black': {'user': {'name': 'player_username'}},
    }
    username = 'player_username'
    assert played_for(players, username) == 'black'


def test_not_played_for_white_side():
    players = {
        'white': {'user': {'name': 'enemy_username'}},
        'black': {'user': {'name': 'player_username'}},
    }
    username = 'player_username'
    assert played_for(players, username) != 'white'


def test_not_played_for_black_side():
    players = {
        'white': {'user': {'name': 'player_username'}},
        'black': {'user': {'name': 'enemy_username'}},
    }
    username = 'player_username'
    assert played_for(players, username) != 'black'


def test_get_short_opening_name():
    pawn_game = "Queen's Pawn Game: Accelerated London System"
    assert get_short_opening_name(pawn_game) == "Queen's Pawn Game"
    ware_defence = 'Ware Defense'
    assert get_short_opening_name(ware_defence) == 'Ware Defense'


def test_group_lost_games_by_opening(get_example_games):
    lost_games = {
        "Queen's Pawn Game": 2,
        "Zukertort Opening: Black Mustang Defense": 1
    }
    assert group_lost_games_by_opening(get_example_games) == lost_games
