def insert_player(conn, username):
    """Добавляет игрока в таблицу, возвращает id"""
    sql = "INSERT OR IGNORE INTO player (username) VALUES (?);"
    params = (username,)
    curr = conn.execute(sql, params)
    player_id = curr.lastrowid
    curr.close()
    conn.commit()
    return player_id


def insert_opening(conn, name, short_name):
    """Добавляет дебют в таблицу, возвращает id"""
    sql = "INSERT OR IGNORE INTO opening (name, short_name) VALUES (?, ?);"
    params = (name, short_name)
    curr = conn.execute(sql, params)
    opening_id = curr.lastrowid
    curr.close()
    conn.commit()
    return opening_id


def insert_game(conn, lichess_id, is_lose, is_draw, player_id, opening_id):
    """Добавляет игру в таблицу"""
    sql = """INSERT OR IGNORE INTO game(lichess_id, is_lose, is_draw, player_id, opening_id)
             VALUES (?, ?, ?, ?, ?);"""
    params = (lichess_id, is_lose, is_draw, player_id, opening_id)
    conn.execute(sql, params)
    conn.commit()


def get_number_of_games(conn, opening_short_name=None):
    """Получить общее количество сыграных игр или в конкретном дебюте"""
    sql = """SELECT 
               count(game.id) as number_of_games
             FROM 
               game INNER JOIN opening ON game.opening_id = opening.id AND 
                                          opening.short_name = ?
          """
    params = (opening_short_name,)
    games = conn.execute(sql, params)
    return games.fetchone()['number_of_games']


def win_games_grouped_by_opening(conn):
    """Получить статистику о выигранных играх для игрока из таблицы 'player' 
       сгруппированную по дебютам"""
    sql = """SELECT 
               opening.short_name,
               count(opening.short_name) as wins_counter
             FROM 
               game INNER JOIN player ON game.player_id = player.id AND
                                         game.is_lose = false AND
                                         game.is_draw = false
                    LEFT JOIN opening ON game.opening_id = opening.id
             GROUP BY
               opening.short_name;
           """
    curr = conn.cursor()
    curr.execute(sql)
    games = curr.fetchall()
    curr.close()
    return games

