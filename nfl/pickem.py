from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from nfl.db import get_db
from nfl.auth import login_required


bp = Blueprint('pickem', __name__)

@bp.route('/')
@login_required
def index():
    return redirect(url_for('pickem.newpickem'))

@bp.route('/oldpickem')
@login_required
def oldpickem():
    return render_template('oldpickem.html')

@bp.route('/pickem')
@login_required
def pickem():
    return render_template('pickem.html')

@bp.route('/newpickem')
@login_required
def newpickem():
    db = get_db()

    # list or dict????
    picks = []
    headings = []

    players = db.execute(
        '''
            SELECT id, displayname FROM user WHERE id <> 0 ORDER BY id ASC
        '''
    ).fetchall()

    games = db.execute(
        '''
            SELECT id, game_desc, teamhome, teamvisitor, winner FROM game
        '''
    ).fetchall()

    def teamUrl(teamid):
        teamname = db.execute(
            '''
                SELECT teamname FROM team WHERE id =?
            ''', (teamid,)
        ).fetchone()
        url = f"./static/{teamname['teamname']}.png"
        return url

    for game in games:
        aDict = {'description':game['game_desc'], 'teamhome':teamUrl(game['teamhome']), 'teamvisitor':teamUrl(game['teamvisitor']), 'winner':teamUrl(game['winner'])}
        
        for player in players:  
            pick = db.execute(
                '''
                    SELECT t.id FROM pick p
                        LEFT JOIN user u ON p.user_id = u.id
                        LEFT JOIN game g ON p.game_id = g.id
                        LEFT JOIN team t ON p.team_id = t.id
                        WHERE p.user_id = ? AND
                        p.game_id = ?
                ''', (player['id'],game['id'])
            ).fetchall()
            if len(pick) > 0:
                aDict[player['displayname']] = teamUrl(pick[0][0])
            else:
                aDict[player['displayname']] = './static/nfl.svg'

        picks.append(aDict)

    for key in picks[0]:
        if key == 'description':
            pass
        elif key == 'teamhome':
            headings.append('Home')
        elif key == 'teamvisitor':
            headings.append('Away')
        elif key == 'winner':
            headings.append('Winner')
        else:
            headings.append(key)

    # need to pass a dictionary...
    return render_template('newpickem.html', picks = picks, players = players, headings = headings)
