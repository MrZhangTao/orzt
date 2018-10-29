from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

moment = Moment()
db = SQLAlchemy()
loginManager = LoginManager()
# loginManager.login_view = "auth.login"

def create_app(configname):
    app = Flask(__name__)
    app.config.from_object(config[configname])
    config[configname].init_app(app)

    #init
    moment.init_app(app)
    db.init_app(app)
    loginManager.init_app(app)

    if app.config["SSL_REDIRECT"]:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    return app