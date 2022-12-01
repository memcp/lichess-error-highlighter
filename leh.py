import berserk
from flask import Flask, render_template, stream_template, jsonify, url_for, Response
    
from services.lichess import (
    get_username_of, is_lose, played_for, group_lost_games_by_opening,
    get_short_opening_name
)
from db import *
from db.queries import (
    insert_player, insert_opening, insert_game, win_games_grouped_by_opening,
    get_number_of_games
)


def create_app():
    import db

    app = Flask(__name__)
    app.config['DATABASE'] = 'db/leh.db'
    db.init_app(app)

    return app


app = create_app()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/opening-stats')
def games():
    conn = get_db()
    opening_stats = {}
    win_opening_groups = win_games_grouped_by_opening(conn)
    
    for group in win_opening_groups:
        number_of_wins = group['wins_counter']
        number_of_games = get_number_of_games(conn, group['short_name'])

        try:
            win_rate = str((number_of_wins / number_of_games) * 100) + '%'
        except:
            win_rate = "-"

        opening_stats[str(group['short_name'])] = {
            'wins': number_of_wins,
            'games': number_of_games,
            'win_rate': win_rate
        }

    return opening_stats


@app.route('/create-games/<token>')
def create_games(token):
    session = berserk.TokenSession(token)
    client = berserk.Client(session)
    account = client.account.get()
    username = account.get('username')

    conn = get_db()
    games = client.games.export_by_player(username, opening=True, rated=True)
    player_id = insert_player(conn, username)

    for game in games:
        game_id = game.get('id')
        game_is_lost = is_lose(game, username)
        game_is_draw = game.get('winner') is None

        if 'opening' not in game:
            continue
        
        opening_name = game.get('opening').get('name')
        opening_short_name = get_short_opening_name(opening_name)
        opening_id = insert_opening(conn, opening_name, opening_short_name)
        insert_game(conn, game_id, game_is_lost, game_is_draw, player_id, opening_id)

    return ""
