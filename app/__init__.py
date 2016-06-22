from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask_login import login_required
from config import config

db = SQLAlchemy()
bootstrap = Bootstrap()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    
    @app.route('/', methods=['GET', 'POST'])
    @login_required
    def index():
        return render_template('index.html')

    return app