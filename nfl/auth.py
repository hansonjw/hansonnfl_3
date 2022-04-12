import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from nfl.db import db, User, League, Team, Game, Pick, getGames, getTeamsDict, getPlayers, getPlayerPicksDict

bp = Blueprint('auth', __name__, url_prefix='/auth')


def log_user_in(u):
    session.clear()
    session['user_id'] = u.id
    return

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        form_unm = request.form['username']
        form_pwh = generate_password_hash(request.form['password'])
        form_dsn = request.form['displayname']
        error = None
        
        if not form_unm:
            error = 'Username is required.'
        elif not form_pwh:
            error = 'Password is required.'
        elif not form_dsn:
            error = 'Display Name is required.'

        if error is None:
            try:
                newUser = User(username=form_unm, pwhash=form_pwh, displayname=form_dsn)
                db.session.add(newUser)
                db.session.commit()
            except:
                error = f"User {form_unm} is already registered."
            else:
                # add some logic here to log the user in and redirect to index...see login route
                log_user_in(newUser)
                flash(f"Hello {newUser.displayname}, welcome to the Hanson NFL pickem site")
                return redirect(url_for('index'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        form_unm = request.form['username']
        form_pwd = request.form['password']
        
        error = None
        user = User.query.filter_by(username=form_unm).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.pwhash, form_pwd):
            error = 'Incorrect password.'

        if error is None:
            log_user_in(user)
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# This decorator ensures this function is run before each request...
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


@bp.route('/logout')
def logout():
    session.clear()
    flash('You have just been logged out')
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view