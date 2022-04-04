from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from nfl.db import get_db, getGames, getTeamsDict, getPlayers, getPlayerPicksDict
from nfl.auth import login_required

bp = Blueprint('pickem', __name__)

@bp.route('/')
@login_required
def index():
    return redirect(url_for('pickem.pickem'))


# temp during refactor
@bp.route('/pickem')
@login_required
def pickem():
    db = get_db()

    # id, html tag
    team_dict = getTeamsDict()
    game_desc = getGames()
    # id, displayname
    players = getPlayers()
    # Dict of Dicts: {player_id: {game_id: team_id} }
    picks = getPlayerPicksDict()

    return render_template('pickem.html', game_desc=game_desc, team_dict=team_dict, players=players, picks=picks)

