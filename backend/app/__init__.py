from flask import Flask, make_response, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

moment = Moment()
db = SQLAlchemy()

def create_app(configname):
    app = Flask(__name__)
    app.config.from_object(config[configname])
    config[configname].init_app(app)

    #init
    moment.init_app(app)
    db.init_app(app)

    if app.config["SSL_REDIRECT"]:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    # 自定义错误返回
    @app.errorhandler(404)
    def notfound(error):
        return make_response(jsonify({"error": "Not Found!"}), 404)

    # 注册蓝图，路由前缀名为/api/v1，不设置则为/
    from .v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    return app
