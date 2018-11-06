from flask import Flask, abort, url_for, request, jsonify, g, current_app, make_response
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask_restful import Api, Resource, reqparse
from .models import User
import functools
from .auth import auth
from . import db
from datetime import datetime
import math

operaTypeEnums = ["lt", "rt"]

# 不积跬步无以至千里

def formattedResponse(data, status_code=200, status_msg="OK"):
    return {
        "code": status_code,
        "msg": status_msg,
        "data": data
    }

class Users(Resource):
    uri = "/api/v1/users"
    endpoint = "/api/v1/users"
    decorators = [auth.login_required]
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.reqparser = reqparse.RequestParser()
        # 该参数是get方法用的
        self.reqparser.add_argument("page", type=int, location="json")

    def get(self):
        args = self.reqparser.parse_args() # get passed args
        # print(args) # {'page': None} 
        # print("page" in args) # True
        if args.get("page") is None:
            userdatas = User.query.order_by(User.register_time.desc()).all()
        else:
            usercount = User.query.count()
            countunit = current_app.config["USERSCOUNTPERPAGE"]
            page = max(1, min(int(args.get("page")), math.ceil(usercount / countunit))) # 将page的下限设为1
            userdatas = User.query.order_by(User.register_time.desc()).offset(countunit * (page - 1)).limit(countunit)
        return formattedResponse([userdata.to_json() for userdata in userdatas])
    
    def post(self):
        pass

class OneUser(Resource):
    uri = "/api/v1/users/<int:id>"
    endpoint = "/api/v1/users/<int:id>"
    decorators = [auth.login_required]
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def get(self, id):
        pass

    def put(self, id):
        pass
