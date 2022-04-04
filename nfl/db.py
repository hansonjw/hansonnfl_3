# This is a python module that interfaces with SQLITE...not to be confused with SQLite itself which is written in C
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    with current_app.open_resource('seed.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


# Helper functions...
def getGames():
    db=get_db()
    games = db.execute(
                '''
                SELECT id, game_desc AS 'Game', winner AS 'Winner', teamhome AS 'Home Team', teamvisitor AS 'Visitor' FROM game
                ORDER by id ASC
                '''
            ).fetchall()
    return games

def getTeamsDict():
    db=get_db()
    teams = db.execute(
            '''
            SELECT id, teamname FROM team
            ORDER by id ASC
            '''
        ).fetchall()

    team_dict = {}
    for team in teams:
        if team['id'] == 0:
            html_tag = "<div class='col'><img src='.././static/nfl.svg' class='team-pickem'></div>"
        else:
            html_tag = "<div class='col'><img src='.././static/" + team['teamname'] + ".png' class='team-pickem'></div>"
        team_dict[team['id']] = html_tag
    return team_dict

def getPlayers():
    db=get_db()
    players = db.execute(
        '''
        SELECT id, displayname FROM user WHERE id <> 0
        '''
    ).fetchall()
    return players

def getPlayerPicksDict():
    playerPicksDict = {}
    players = getPlayers()
    
    db=get_db()

    for player in players:
        picksDict = {}
        rawPicks = db.execute(
            '''
            SELECT * FROM pick WHERE user_id=?
            ''', (player['id'],)
        ).fetchall()
        for pick in rawPicks:
            picksDict[pick['game_id']] = pick['team_id']
        playerPicksDict[player['id']] = picksDict

    return playerPicksDict