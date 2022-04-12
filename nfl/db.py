# This is a python module that interfaces with SQLITE...not to be confused with SQLite itself which is written in C
import sqlite3
# db.execute and other methods are SQLITE...need to convert this all to SQLAlchemy, I believe

import click
from flask import Flask, current_app, g, flash
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    db.create_all(app=app)
    loadStaticData(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pwhash = db.Column(db.String(), nullable=False)
    displayname = db.Column(db.String(), nullable=False)

class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    league = db.relationship('Team', backref=db.backref('league', lazy=True))

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teamname = db.Column(db.String())
    league_id = db.Column(db.Integer, db.ForeignKey('league.id'))
    
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_desc = db.Column(db.String())
    game_league_id = db.Column(db.Integer, db.ForeignKey('league.id'))
    game_round = db.Column(db.String())
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    visitor_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    winner_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    # relationships...teamhome, teamvisitor, winner, game_conf
    home_team = db.relationship('Team', foreign_keys=[home_team_id])
    visitor_team = db.relationship('Team', foreign_keys=[visitor_team_id])
    winner_team = db.relationship('Team', foreign_keys=[winner_team_id])

class Pick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    # relationships...
    user = db.relationship('User', backref=db.backref('picks', lazy=True))
    game = db.relationship('Game', backref=db.backref('picks', lazy=True))
    team = db.relationship('Team', backref=db.backref('picks', lazy=True))


def loadStaticData(app):
    with app.app_context():
        # pre-populate games, leagues and teams with static data...
        try:
            nfl=Team(id=0, teamname='nfl', league_id=0)
            _49ers=Team(id=1, teamname='49ers', league_id=2)
            bengals=Team(id=2, teamname='bengals', league_id=1)
            bills=Team(id=3, teamname='bills', league_id=1)
            bucs=Team(id=4, teamname='bucs', league_id=2)
            chiefs=Team(id=5, teamname='chiefs', league_id=1)
            packers=Team(id=6, teamname='packers', league_id=2)
            rams=Team(id=7, teamname='rams', league_id=2)
            titans=Team(id=8, teamname='titans', league_id=1)
            db.session.add(nfl)
            db.session.add(_49ers)
            db.session.add(bengals)
            db.session.add(bills)
            db.session.add(bucs)
            db.session.add(chiefs)
            db.session.add(packers)
            db.session.add(rams)
            db.session.add(titans)
            game_1=Game(id=1, game_desc='AFC Divisional Round, Game 1', game_league_id=1, game_round='Division', home_team_id=5, visitor_team_id=3, winner_team_id=5)
            game_2=Game(id=2, game_desc='AFC Divisional Round, Game 2', game_league_id=1, game_round='Division', home_team_id=8, visitor_team_id=2, winner_team_id=2)
            game_3=Game(id=3, game_desc='NFC Divisional Round, Game 1', game_league_id=2, game_round='Division', home_team_id=6, visitor_team_id=1, winner_team_id=1)
            game_4=Game(id=4, game_desc='NFC Divisional Round, Game 2', game_league_id=2, game_round='Division', home_team_id=4, visitor_team_id=7, winner_team_id=7)
            game_5=Game(id=5, game_desc='AFC Championship', game_league_id=1, game_round='Conference', home_team_id=5, visitor_team_id=2, winner_team_id=2)
            game_6=Game(id=6, game_desc='NFC Championship', game_league_id=2, game_round='Conference', home_team_id=7, visitor_team_id=1, winner_team_id=7)
            game_7=Game(id=7, game_desc='Super Bowl', game_league_id=0, game_round='Super Bowl', home_team_id=7, visitor_team_id=2, winner_team_id=7)
            db.session.add(game_1)
            db.session.add(game_2)
            db.session.add(game_3)
            db.session.add(game_4)
            db.session.add(game_5)
            db.session.add(game_6)
            db.session.add(game_7)
            league_0=League(id=0, name='NFL')
            league_1=League(id=1, name='AFC')
            league_2=League(id=2, name='NFC')
            db.session.add(league_0)
            db.session.add(league_1)
            db.session.add(league_2)
            db.session.commit()
        except:
            error = "database potentially already exists, static data not written on this app start..."
            print(error)
    return


# Helper functions for accessing database data...
def getGames():
    games = db.session.query(Game.id, Game.game_desc.label("Game"), Game.winner_team_id.label("Winner"), Game.home_team_id.label("Home Team"), Game.visitor_team_id.label("Visitor")).order_by(Game.id).all()
    return games

def getTeamsDict():
    teams = Team.query.order_by(Team.id).all()
    team_dict = {}
    for team in teams:
        if team.id == 0:
            html_tag = "<div class='col'><img src='.././static/nfl.svg' class='team-pickem'></div>"
        else:
            html_tag = "<div class='col'><img src='.././static/" + team.teamname + ".png' class='team-pickem'></div>"
        team_dict[team.id] = html_tag
    return team_dict

def getPlayers():
    players = User.query.filter(User.id != 0).all()
    return players

def getPlayerPicksDict():
    # return a dict of dicts: { player.id: {game.id: team.id, ...}, ...}
    playerPicksDict = {}
    players = getPlayers()
    
    for player in players:
        picksDict = {}
        rawPicks = Pick.query.filter_by(user_id=player.id).all()
        for pick in rawPicks:
            picksDict[pick.game_id] = pick.team_id
        playerPicksDict[player.id] = picksDict

    return playerPicksDict