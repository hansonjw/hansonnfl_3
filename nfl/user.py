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

    print(type(user))
    print(type(user[0]))
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
    db = get_db()
    try:
        games = db.execute(
            '''
            SELECT g.id, g.game_desc, g.game_conf, g.teamhome, g.teamvisitor, g.winner,
            th.id AS home_id, th.teamname AS home, tv.id AS visitor_id, tv.teamname AS visitor, tw.id AS victor_id, tw.teamname AS victor
            FROM game g
            LEFT JOIN team th ON g.teamhome=th.id
            LEFT JOIN team tv ON g.teamvisitor=tv.id
            LEFT JOIN team tw on g.winner=tw.id
            '''
        ).fetchall()
    except:
        games = "XXX"
    else:
        pass
    return render_template('user/picks.html', games=games)


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