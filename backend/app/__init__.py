from flask import Flask, make_response, jsonify, g
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
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

    # create a restful api instance
    api = Api(app)
    from . import v1
    # add_resource 函数使用指定的endpoint注册路由到框架上，如果没有指定端点，flask-restful会根据类名生成一个
    api.add_resource(v1.Users, v1.Users.uri, endpoint=v1.Users.endpoint)
    api.add_resource(v1.NewUser, v1.NewUser.uri, endpoint=v1.NewUser.endpoint)
    api.add_resource(v1.Introduction, v1.Introduction.uri, endpoint=v1.Introduction.endpoint)
    api.add_resource(v1.ExtraIntro, v1.ExtraIntro.uri, endpoint=v1.ExtraIntro.endpoint)
    from .auth import auth

    # 每次请求前进行安全验证
    @app.before_request
    # @auth.login_required
    def before_request():
        print("HelloWorld")
    
    # 测试用的接口:获取token
    # @app.route("/api/v1/token")
    # def get_token():
    #     return jsonify({"token": g.user.generate_auth_token(expiration=3600), "expiration": 3600})

    return app
