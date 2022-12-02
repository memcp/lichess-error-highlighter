def get_username_of(players, side):
    """Ищет среди списка `players` и возвращает имя игрока играющего за сторону `side`"""
    player = players.get(side)
    username = player.get('user').get('name')
    return username.lower()


def is_lose(game, username):
    """Определяет проиграна ли игроком `username` игра `game`"""
    players = game.get('players')
    side = played_for(players, username)
    winner_side = game.get('winner')
    return side != winner_side


def played_for(players, username):
    """Определяет играл ли игрок с `username` из списка `players` за сторону чёрный или за
       белый цвет"""
    white_username = get_username_of(players, 'white')
    black_username = get_username_of(players, 'black')

    if username == white_username:
        return 'white'

    if username == black_username:
        return 'black'


def get_short_opening_name(opening):
    """Получить короткую версию названия дебюта"""
    return opening.split(':')[0]

