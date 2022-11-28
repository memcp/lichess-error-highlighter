def get_username_of(players, side):
    """Ищет среди списка `players` и возвращает имя игрока играющего за сторону `side`"""
    player = players.get(side)
    username = player.get('user').get('name')
    return username.lower()


def is_lose(game, username):
    """Определяет проиграл ли игрок с `username` игра `game`"""
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
    """Поличить короткую версию названия дебюта"""
    return opening.split(':')[0]


def group_lost_games_by_opening(games, username, short=True):
    """Формирует словарь из числа проигранных игроком игр, группируя их по дебюту, 
       параметр `short` нужен для того чтобы разные варианты одного дебюта 
       добавлялись в общую группу"""
    openings_to_loses = {}
    
    for game in games:
        opening = game.get('opening').get('name')
        
        if short:
            opening = get_short_opening_name(opening)
        
        if not is_lose(game, username):
            continue

        if opening in openings_to_loses:
            openings_to_loses[opening] += 1

        if opening not in openings_to_loses:
            openings_to_loses[opening] = 1

    return openings_to_loses


 
