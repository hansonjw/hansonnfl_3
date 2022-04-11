import os
from flask import Flask
from . import db

import os
import re

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    uri = os.getenv("DATABASE_URL")  # or other relevant config var
    if uri.startswith("postgres://"):   
        uri = uri.replace("postgres://", "postgresql://", 1)

# rest of connection code using the connection string `uri`
    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI = uri or 'sqlite:///./../instance/nfl.db',
        SQLALCHEMY_TRACK_MODIFICATIONS = False 
        # os.path.join('sqlite:////', app.instance_path, 'nfl.db'),
        # DATABASE=os.path.join(app.instance_path, 'nfl.sqlite')
    )    

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import pickem
    app.register_blueprint(pickem.bp)
    app.add_url_rule('/', endpoint='index')

    from . import user
    app.register_blueprint(user.bp)

    from . import db
    db.init_app(app)
    

    return app