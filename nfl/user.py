from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from nfl.db import db, User, League, Team, Game, Pick, getGames, getTeamsDict, getPlayers, getPlayerPicksDict
from nfl.auth import login_required

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/updateinfo', methods=('GET', 'POST'))
@login_required
def updateinfo():

    if request.method == 'POST':
        username = request.form['username']
        displayname = request.form['displayname']
        u = User.query.get(g.user.id)
        error = None

        if not username and not displayname:
            error = 'A new username and/or new displayname is required.'
        
        if error is None:
            try:
                if username!= "":
                    u.username=username
                    flash(f"Your username was updated successfully to: {u.username}")
                if displayname!= "":
                    u.displayname=displayname
                    flash(f"Your diplayname was updated successfully to: {u.displayname}")
                db.session.commit() 
            except db.IntegrityError:
                error = f"User {username} or Display Name {displayname} is already registered."
            else:
                return redirect(url_for("pickem.pickem"))

        flash(error)

    return render_template('user/info.html')


@bp.route('/updatepicks', methods=('GET', 'POST'))
@login_required
def updatepicks():
    error = None
    if request.method=='POST':
        try:
            keys = request.form.keys()
            for key in keys:
                tid = int(request.form[key])
                uid = g.user.id
                gid = int(key)
                pick = Pick(user_id=uid, game_id=gid, team_id=tid)
                db.session.add(pick)
            db.session.commit()
            flash("Picks were updated successfully!")
            return redirect (url_for("pickem.pickem"))
        except:
            error = "Picks not updated...error"
            print(error)
            flash(error)
            return redirect (url_for("user.updatepicks"))
    else:
        try:
            game_desc = getGames()
            team_dict = getTeamsDict()
        except:
            error="error, query functions not executing correctly"
            print(error)
            flash(error)
        else:
            pass
        return render_template('user/picks.html', game_desc=game_desc, team_dict=team_dict)


@bp.route('/changepassword', methods=('GET', 'POST'))
@login_required
def changepassword():

    if request.method == 'POST':
        pwhash = generate_password_hash( request.form['newpassword_1'] )
        pwconfirm = check_password_hash(pwhash, request.form['newpassword_2'])
        error = None
        u = User.query.get(g.user.id)

        if not pwconfirm:
            error = 'Password and confirmation password must match. Please try again.'

        if error is None:
            try:
                u.pwhash = pwhash
                db.session.commit()
            except db.IntegrityError:
                error = "something went wrong, new password not logged"
            else:
                flash("Your password was updated successfully")
                return redirect (url_for("pickem.pickem"))
        flash(error)
    return render_template('user/password.html')