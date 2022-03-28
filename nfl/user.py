from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from nfl.db import get_db
from nfl.auth import login_required


bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/user', methods=('GET', 'POST'))
@login_required
def user():
    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE id=?', (g.user['id'],)
    ).fetchall()

    return render_template('user/user.html', user=user)


@bp.route('/updateinfo', methods=('GET', 'POST'))
@login_required
def updateinfo():

    if request.method == 'POST':
        username = request.form['username']
        displayname = request.form['displayname']
    
        db = get_db()
        error = None

        if not username and not displayname:
            error = 'A new username and/or new displayname is required.'
        
        if error is None:
            try:
                if username!= "" and displayname != "":
                    db.execute(
                        "UPDATE user SET username=?, displayname=? WHERE id=?",
                        (username, displayname, g.user['id'])
                    )
                    db.commit()
                elif username!= "":
                    db.execute(
                        "UPDATE user SET username=? WHERE id=?",
                        (username, g.user['id'])
                    )
                    db.commit()
                elif displayname!= "":
                    db.execute(
                        "UPDATE user SET displayname=? WHERE id=?",
                        (displayname, g.user['id'])
                    )
                    db.commit()
                else:
                    print("ERROR...somethings up")
                    print(username, type(username), len(username))
                    print(displayname, type(displayname), len(displayname)) 
            except db.IntegrityError:
                error = f"User {username} or Display Name {displayname} is already registered."
            else:
                return redirect(url_for("user.user"))


        flash(error)

    return render_template('user/info.html')


@bp.route('/updatepicks', methods=('GET', 'POST'))
@login_required
def updatepicks():

    if request.method=='POST':
        try:

            keys = request.form.keys()
            
            for key in keys:

                tid = int(request.form[key])
                uid = g.user['id']
                gid = int(key)

                db = get_db()
                db.execute(
                    '''
                    UPDATE pick SET team_id=? WHERE user_id=? AND game_id=?
                    ''',
                    (tid, uid, gid)
                )
                db.commit()

            return redirect (url_for("pickem.newpickem"))
        except:
            print("Error...")
            return redirect (url_for("user.user"))

    else:
        db = get_db()
        try:
            game_desc = db.execute(
                '''
                SELECT id, game_desc AS 'Game', winner AS 'Winner', teamhome AS 'Home Team', teamvisitor AS 'Visitor' FROM game
                ORDER by id ASC
                '''
            ).fetchall()
            
            players = db.execute(
                '''
                SELECT id, displayname FROM user
                '''
            ).fetchall()

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

            playerpicks = db.execute(
                '''
                SELECT p.game_id, t.teamname FROM pick p
                LEFT JOIN team t ON
                p.team_id = t.id
                WHERE p.user_id=?
                ORDER BY p.game_id ASC
                ''', (g.user['id'],)
            ).fetchall()

        except:
            games = "XXX"
            print(games)
        else:
            pass
        return render_template('user/picks.html', playerpicks=playerpicks, game_desc=game_desc, team_dict=team_dict)


@bp.route('/changepassword', methods=('GET', 'POST'))
@login_required
def changepassword():

    if request.method == 'POST':
        pwhash = generate_password_hash( request.form['newpassword_1'] )
        pwconfirm = check_password_hash(pwhash, request.form['newpassword_2'])
        error = None
        db = get_db()

        if not pwconfirm:
            error = 'Password and confirmation password must match. Please try again.'

        if error is None:
            try:
                db.execute(
                    "UPDATE user SET pwhash=? WHERE id=?",
                    (pwhash, g.user['id'])
                )
                db.commit()
            except db.IntegrityError:
                error = "something went wrong, new password not logged"
            else:
                return redirect (url_for("user.user"))
        
        flash(error)

    return render_template('user/password.html')