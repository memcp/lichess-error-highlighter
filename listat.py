from decimal import Decimal

import berserk
from flask import Flask, render_template, redirect, url_for, session
    
from services.lichess import is_lose, get_short_opening_name
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
app.secret_key = "test_secret_key"


@app.route('/')
def index():
    access_token = session.get('access_token')
    return render_template('index.html', access_token=access_token)


@app.route('/opening-stats')
def opening_stats():
    conn = get_db()
    threshold = 50
    statistics = []
    win_opening_groups = win_games_grouped_by_opening(conn)
    
    for group in win_opening_groups:
        number_of_wins = group['wins_counter']
        number_of_games = get_number_of_games(conn, group['short_name'])

        try:
            win_rate = Decimal((number_of_wins / number_of_games) * 100)
        except ZeroDivisionError:
            win_rate = "-"

        if number_of_games < threshold:
            continue

        opening = (group['short_name'], str(round(win_rate, 2)) + "%", number_of_games)
        statistics.append(opening)

    return render_template('opening-stats.html', statistics=statistics)


@app.route('/create-games/<token>')
def create_games(token):
    lichess_session = berserk.TokenSession(token)
    session['access_token'] = token
    client = berserk.Client(lichess_session)
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

    return redirect(url_for('opening_stats'))
