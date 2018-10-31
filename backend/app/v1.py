from flask import Flask, abort, url_for, request, jsonify, g, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_restful import Api, Resource, reqparse
from .models import User, SpecialData
import functools

operaTypeEnums = ["lt", "rt"]

def operaTypeValidate(str):
    '''return True if str is a valid value'''
    if str in operaTypeEnums:
        return str
    else:
        return None


class Tokens(Resource):
    uri = "/api/v1/tokens"
    endpoint = "/api/v1/tokens"
    
    def __init__(self, *args, **kw):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument("email", type=str, required=True, location="json", help="email is needed!")
        self.reqparser.add_argument("password", type=str, required=True, location="json", help="where is your password?")
        self.reqparser.add_argument("operaType", type=operaTypeValidate, required=True, location="json", help="you need pass a operaType")
        super().__init__(*args, **kw)

    def post(self):
        '''登录/注册:通过参数判断'''
        args = self.reqparser.parse_args() # get passed args
        print(args["operaType"], operaTypeEnums[0])
        if args["operaType"] == operaTypeEnums[0]:# login
            # print(args)
            # print(request.json)
            user = User.query.filter_by(email=args["email"]).first()
            if not user or not user.verify_password(args["password"]):
                return {"message": "email or password is wrong, please again!"}
            return jsonify({"token": user.generate_auth_token(expiration=3600), "expiration": 3600})
        elif args["operaType"] == operaTypeEnums[1]:  # register
            pass

class OneToken(Resource):
    uri = "/api/v1/tokens/<token>"
    endpoint = "/api/v1/tokens/<token>"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def get(self, token):
        '''获取用户状态:获取用户的上次登录时间，
        再从配置里获取过期时间，然后获取现在的服务器时间，
        一比较，就知道用户指令是否过期了'''
        serializer = Serializer(current_app.config["SECRET_KEY"])


    def delete(self, token):
        '''删除token，注销logout'''
        pass

class Users(Resource):
    uri = "/api/v1/users"
    endpoint = "/api/v1/users"

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

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def get(self, id):
        user = User.query.filter_by(id=id).first_or_404()
        return jsonify({"user": user.to_json()})

    def put(self, id):
        pass
