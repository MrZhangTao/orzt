from flask import Flask, make_response, jsonify
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
    @app.errorhandler(404)
    def notfound(error):
        return make_response(jsonify({"error": "Not Found!"}), 404)


    api = Api(app)
    from . import v1
    # add_resource 函数使用指定的endpoint注册路由到框架上，如果没有指定端点，flask-restful会根据类名生成一个
    api.add_resource(v1.UserListAPI, v1.UserListAPI.uri, endpoint=v1.UserListAPI.endpoint)
    api.add_resource(v1.UserAPI, v1.UserAPI.uri, endpoint=v1.UserAPI.endpoint)
    return app
