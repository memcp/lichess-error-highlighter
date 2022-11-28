import pytest

from services.lichess import (
    get_username_of,
    is_lose,
    played_for,
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
    assert played_for(players, 'white', username) == 'white'


def test_played_for_black_side():
    players = {
        'white': {'user': {'name': 'enemy_username'}},
        'black': {'user': {'name': 'player_username'}},
    }
    username = 'player_username'
    assert played_for(players, 'black', username) == 'black'


def test_not_played_for_white_side():
    players = {
        'white': {'user': {'name': 'enemy_username'}},
        'black': {'user': {'name': 'player_username'}},
    }
    username = 'player_username'
    assert played_for(players, 'white', username) == 'black'


def test_not_played_for_black_side():
    players = {
        'white': {'user': {'name': 'player_username'}},
        'black': {'user': {'name': 'enemy_username'}},
    }
    username = 'player_username'
    assert played_for(players, 'black', username) == 'white'
