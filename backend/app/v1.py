from flask import Flask, abort, url_for, request, jsonify, g, current_app, make_response
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask_restful import Api, Resource, reqparse
from .models import User, SpecialData
import functools
from .auth import auth
from . import db
from datetime import datetime

operaTypeEnums = ["lt", "rt"]



class Tokens(Resource):
    uri = "/api/v1/tokens"
    endpoint = "/api/v1/tokens"
    
    def __init__(self, *args, **kw):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument("email", type=str, required=True, location="json", help="email is needed!")
        self.reqparser.add_argument("password", type=str, required=True, location="json", help="where is your password?")
        self.reqparser.add_argument(
            "operaType", type=str, choices=operaTypeEnums, required=True, location="json", help="you need pass a right operaType")
        # 注册用的额外数据
        self.reqparser.add_argument("password2", type=str, location="json")
        self.reqparser.add_argument("username", type=str, location="json")
        self.reqparser.add_argument("name", type=str, location="json")
        self.reqparser.add_argument("sex", type=int, choices=range(2), location="json")
        self.reqparser.add_argument("location", type=str, location="json")
        self.reqparser.add_argument("about_me", type=str, location="json")

        super().__init__(*args, **kw)

    def post(self):
        '''登录/注册:通过参数判断'''
        args = self.reqparser.parse_args() # get passed args
        print(request.json)
        if args["operaType"] == operaTypeEnums[0]:# login
            # print(args)
            # print(request.json)
            user = User.query.filter_by(email=args["email"]).first()
            if not user or not user.verify_password(args["password"]):
                return {"message": "email or password is wrong, please again!"}
            user.ping()
            db.session.commit()
            return jsonify({"token": user.generate_auth_token(expiration=3600), "expiration": 3600})
        elif args["operaType"] == operaTypeEnums[1]:  # register
            user = User.query.filter_by(email=args["email"]).first()
            if user is not None:
                return jsonify({"error": "this email had been reigsterd!"})
            user = User(
                email=args["email"],
                username=args["username"],
                password="password",
                name=args["name"],
                sex=args["sex"],
                location=args["location"],
                about_me=args["about_me"],
            )
            db.session.add(user)
            db.session.commit()
            return make_response(jsonify({
                "new user": user.to_json(),
                "token": user.generate_auth_token(expiration=3600),
                "expiration": 3600}),
            201)

class OneToken(Resource):
    uri = "/api/v1/tokens/<token>"
    endpoint = "/api/v1/tokens/<token>"
    decorators = [auth.login_required]
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def get(self, token):
        '''获取用户状态:获取用户的上次登录时间，
        再从配置里获取过期时间，然后获取现在的服务器时间，
        一比较，就知道用户指令是否过期了'''
        serializer = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = serializer.loads(token)
        except SignatureExpired as e:
            return jsonify({"error": "valid token, but expired"})
        except BadSignature as e:
            return jsonify({"error": "invalid token"})
        last_logined = User.query.get(data["id"]).last_logined
        expiration = 3600
        now = datetime.utcnow()
        resttime = datetime.timestamp(
            last_logined) + expiration - datetime.timestamp(now)
        if resttime > 0:
            return jsonify({"resttime": resttime})
        else:
            return jsonify({"error": "your auth token has expired!"})

        return {"yes":"hahaha"}

    def delete(self, token):
        '''删除token，注销logout'''
        return jsonify({"hint": "logout ok!"})

class Users(Resource):
    uri = "/api/v1/users"
    endpoint = "/api/v1/users"
    decorators = [auth.login_required]
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def get(self):
        '''获取用户列表，该资源的请求需要管理员权限，尚未设计'''
        users = User.query.order_by(User.registration_time.desc()).all()
        # retvalue = [user.to_json() for user in users]
        retvalue = []
        for user in users:
            jsondata = user.to_json()
            userid = user.id
            if True:
                spedata = SpecialData.query.filter_by(owner_id=userid).first_or_404()
                jsondata["spedata"] = spedata.to_json()
            retvalue.append(jsondata)
        # return {"userlist": retvalue}
        return jsonify({"userlist": retvalue})
    def post(self):
        '''用户注册'''
        pass

class OneUser(Resource):
    uri = "/api/v1/users/<int:id>"
    endpoint = "/api/v1/users/<int:id>"
    decorators = [auth.login_required]
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def get(self, id):
        user = User.query.filter_by(id=id).first_or_404()
        return jsonify({"user": user.to_json()})

    def put(self, id):
        pass
