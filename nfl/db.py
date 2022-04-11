# This is a python module that interfaces with SQLITE...not to be confused with SQLite itself which is written in C
import sqlite3
# db.execute and other methods are SQLITE...need to convert this all to SQLAlchemy, I believe

import click
from flask import Flask, current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    db.create_all(app=app)

# @click.command('init-db')
# @with_appcontext
# def init_db_command():
#     """Clear the existing data and create new tables."""
#     db.create_all()
#     click.echo('Initialized the database.')
#     print("db.init_command() just ran!!")

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




# Helper functions...going to have to retool all of this...is this the controller part of mvc?
def getGames():
    # db=get_db()
    # games = db.execute(
    #             '''
    #             SELECT id, game_desc AS 'Game', winner AS 'Winner', teamhome AS 'Home Team', teamvisitor AS 'Visitor' FROM game
    #             ORDER by id ASC
    #             '''
    #         ).fetchall()
    # games = Game.query.order_by(Game.id).all()
    games = db.session.query(Game.id, Game.game_desc.label("Game"), Game.winner_team_id.label("Winner"), Game.home_team_id.label("Home Team"), Game.visitor_team_id.label("Visitor")).order_by(Game.id).all()
    # games = Game.query(Game.id, Game.game_desc, Game.winner_team_id, Game.home_team_id, Game.visitor_team_id).order_by(Game.id).all()
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
    # db=get_db()
    # players = db.execute(
    #     '''
    #     SELECT id, displayname FROM user WHERE id <> 0
    #     '''
    # ).fetchall()
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


    # db=get_db()

    # for player in players:
    #     picksDict = {}
    #     rawPicks = db.execute(
    #         '''
    #         SELECT * FROM pick WHERE user_id=?
    #         ''', (player['id'],)
    #     ).fetchall()
    #     for pick in rawPicks:
    #         picksDict[pick['game_id']] = pick['team_id']
    #     playerPicksDict[player['id']] = picksDict

    return playerPicksDict