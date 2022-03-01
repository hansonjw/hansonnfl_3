from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from nfl.db import get_db
from nfl.userdata import picks

bp = Blueprint('pickem', __name__)

@bp.route('/')
def index():
    return '<div>This is the app homepage</div>'

@bp.route('/oldpickem')
def oldpickem():
    return render_template('oldpickem.html')

@bp.route('/pickem')
def pickem():
    return render_template('pickem.html', data=picks)

@bp.route('/user')
def user():
    db = get_db()
    users = db.execute(
        'SELECT * FROM user'
    ).fetchall()
    print(users)

    return render_template('users.html', users=users)