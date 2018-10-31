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

    # 自定义错误返回
    for status_code, status_msg in config[configname].errorDict.items():
        status_code = int(status_code)
        @app.errorhandler(status_code)
        def handler(error):
            return make_response(jsonify({"error": status_msg}), status_code)

    # create a restful api instance
    api = Api(app)
    from . import v1
    # add_resource 函数使用指定的endpoint注册路由到框架上，如果没有指定端点，flask-restful会根据类名生成一个
    api.add_resource(v1.Users, v1.Users.uri, endpoint=v1.Users.endpoint)
    api.add_resource(v1.OneUser, v1.OneUser.uri, endpoint=v1.OneUser.endpoint)
    api.add_resource(v1.Tokens, v1.Tokens.uri, endpoint=v1.Tokens.endpoint)
    api.add_resource(v1.OneToken, v1.OneToken.uri, endpoint=v1.OneToken.endpoint)
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
