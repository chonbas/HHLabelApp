# -----------------------------------------------------------
# File: app/__init__.py
# Description:
# Initalization file for server application.
# Injects login manager, sqlalchemy ORM for database interactions,
# and registers route blueprints from sub-modules
#
# Usage:
# from app import create_app, db
# app = create_app('config')
# This step is handled in development by the manager, 
# and in production by the wsgi.py config file.
# -----------------------------------------------------------

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask_login import login_required
from config import config

from sklearn.externals import joblib
from sklearn.ensemble import GradientBoostingClassifier

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'index'

clf = joblib.load('pkl/gbc_classifier.pkl')

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    login_manager.init_app(app)
    db.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    

    #````````````````````````````````````````
    # Route to root domain directory.
    # Servex index.html file which houses angular application.
    # This is being served through this application for development purposes.
    # In production,the client/front-end application will be server separately and this application
    # will serve only as a REST API
    #````````````````````````````````````````
    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('index.html')

    
    return app