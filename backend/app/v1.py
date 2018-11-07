from flask import Flask, abort, url_for, request, jsonify, g, current_app, make_response
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask_restful import Api, Resource, reqparse
from .models import User, ExtraInfo, Record, Picture
import functools
from .auth import auth
from . import db
from datetime import datetime
import math
from sqlalchemy.exc import IntegrityError

operaTypeEnums = ["lt", "rt"]


# 不积跬步无以至千里

def formattedResponse(data, status_code=200, status_msg="OK"):
    '''返回格式化输出'''
    return {
        "code": status_code,
        "msg": status_msg,
        "data": data
    }

# 字段合法验证函数

def isPhoneValid(telephone):
    '''号码合法性检验'''
    return True

def isUsernameValid(username):
    '''昵称合法性检验'''
    return True

def isPasswordValid(password):
    '''密码合法性检验'''
    return True

def isCityValid(cityname):
    '''城市合法性检验'''
    return True

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
        '''获取用户数据列表'''
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
        

class NewUser(Resource):
    uri = "/api/v1/newusers"
    endpoint = "/api/v1/newusers"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.reqparser = reqparse.RequestParser()
        # 必要数据
        self.reqparser.add_argument("telephone", type=str, location="json", required=True, help="telephone is needed!")    
        self.reqparser.add_argument("password", type=str, location="json", required=True, help="password is needed!")
        self.reqparser.add_argument("username", type=str, location="json", required=True, help="username is needed!")
        self.reqparser.add_argument("sex", type=int, choices=[0, 1], location="json", required=True, help="sex should not be empty and valid!")
        self.reqparser.add_argument("location", type=str, location="json", required=True, help="location is needed!")

        # 可传数据
        self.reqparser.add_argument("birth", type=str, location="json")
        self.reqparser.add_argument("about_me", type=str, location="json")

    def post(self):
        '''注册账号'''
        # 验证各参数是否合法
        args = self.reqparser.parse_args()
        telephone = args.get("telephone")
        password = args.get("password")
        username = args.get("username")
        sex = args.get("sex")
        location = args.get("location")

        birth = args.get("birth")
        about_me = args.get("about_me")

        if not isPhoneValid(telephone) or not isPasswordValid(password) or \
                not isUsernameValid(username) or not isCityValid(location):
            return formattedResponse({}, 400, "params passed are valid!")
        # 验证telephone是否已被注册
        anotherUser = User.query.filter(User.telephone == telephone).first()
        if anotherUser is not None:
            return formattedResponse({}, 400, "telephone has been registered!")
        # 建立用户数据
        user = User(
            telephone = telephone,
            password = password,
            username = username,
            sex = sex,
            location = location,
        )
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return formattedResponse({}, 500, "Sorry, please try again!")

        # 保存额外数据
        if birth is not None:
            birth = datetime.strptime(birth, "%Y-%m-%d") # 转换为时间格式
            # 验证生日日期是否超过了今天,是则置为None
            if False:
                birth = None
        
        extrainfo = ExtraInfo(
            user_id=user.user_id,
            birth=birth,
            about_me=about_me,
        )
        user.extrainfo = extrainfo
        db.session.add(user)
        db.session.commit()
        #一切正常，成功返回
        return formattedResponse({"NewUser": user.to_json()})
        

class Introduction(Resource):
    uri = "/api/v1/users/<int:user_id>/intro"
    endpoint = "/api/v1/users/<int:user_id>/intro"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument("telephone", type=str, location="json")
        self.reqparser.add_argument("oldpassword", type=str, location="json")
        self.reqparser.add_argument("password", type=str, location="json")
        self.reqparser.add_argument("username", type=str, location="json")
        self.reqparser.add_argument("location", type=str, location="json")

    def get(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        if user is None:
            return formattedResponse({}, 400, "Here the user does not exist!")
        return formattedResponse({"introduction": user.to_json()})
    
    @auth.login_required
    def post(self, user_id):
        '''修改玩家数据'''
        args = self.reqparser.parse_args()  # get passed args

        password = args.get("password")
        user = User.query.filter_by(user_id=user_id).first()
        if password is None or user is None or not isPasswordValid(password):
            return formattedResponse({}, 400, "password is invalid!")
        if args.get("oldpassword") is None:  # 不改密码
            # 首先验证密码是否正确
            if not user.verify_password(password):
                return formattedResponse({}, 400, "password is wrong!")
            needModify = False  # 是否需要修改资料
            telephone = args.get("telephone")
            username = args.get("username")
            location = args.get("location")
            if telephone is not None:
                # 验证号码是否合法 不合法直接返回错误
                if not isPhoneValid(telephone):
                    return formattedResponse({}, 400, "telephone is invalid!")
                # 验证telephone是否已被注册
                anotherUser = User.query.filter(User.telephone == telephone).first()
                if user.telephone != telephone and anotherUser is None:
                    needModify = True
                    user.telephone = telephone
            if username is not None:
                # 验证昵称是否合法，不合法直接返回错误
                if not isUsernameValid(username):
                    return formattedResponse({}, 400, "username is invalid!")
                if user.username != username:
                    needModify = True
                    user.username = username
            if location is not None:
                # 检验常居地是否合法，不合法直接返回错误
                if not isCityValid(location):
                    return formattedResponse({}, 400, "location is invalid!")
                if user.location != location:
                    needModify = True
                    user.location = location
            if needModify:
                db.session.commit()
                return formattedResponse({"introduction": user.to_json()})
            else:
                return formattedResponse({}, 400, "introduction passed is same as before!")
        else:
            # 验证旧密码和新密码
            oldpassword = args.get("oldpassword")
            newpassword = password
            if not isPasswordValid(oldpassword) or not user.verify_password(oldpassword):
                return formattedResponse({}, 400, "old password is invalid!")
            if oldpassword == newpassword:
                return formattedResponse({}, 400, "new password is same as old password!")
            else:  # 修改密码成功
                user.password = newpassword
                db.session.commit()
                return formattedResponse({})


class ExtraIntro(Resource):
    uri = "/api/v1/users/<int:user_id>/extraintro"
    endpoint = "/api/v1/users/<int:user_id>/extraintro"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.reqparser = reqparse.RequestParser()
        # 可传参数
        self.reqparser.add_argument("birth", type=str)
        self.reqparser.add_argument("lefttime", type=int)
        self.reqparser.add_argument("headuri", type=str)
        self.reqparser.add_argument("bguri", type=str)
        self.reqparser.add_argument("tags", type=str)
        self.reqparser.add_argument("about_me", type=str)

    def get(self, user_id, origin=False):
        '''获取额外数据(origin为True时表示在内部使用，返回格式将变更)'''
        user = User.query.get(user_id)
        if user is None:
            data = formattedResponse({}, 400, "Here the user does not exist!")
            if origin:
                return (False, data)
            else:
                return data

        if origin:
            return (True, user)
        else:
            return formattedResponse({"extraInfo": user.extrainfo.to_json()})

    def post(self, user_id):
        '''更新额外数据'''
        userexists, user = self.get(user_id, True)
        if not userexists:
            return user
        
        args = self.reqparser.parse_args()
        # 取出参数
        birth = args.get("birth")
        lefttime = args.get("lefttime")
        headuri = args.get("headuri")
        bguri = args.get("bguri")
        tags = args.get("tags")
        about_me = args.get("about_me")
        # 参数合法检测
        needModify = 0
        if birth is not None:
            birth = datetime.strptime(birth, "%Y-%m-%d")  # 转换为时间格式
            # 验证生日日期是否超过了今天,是则置为None
            if False:
                birth = None
            else:
                needModify += 1
                user.extrainfo.birth = birth
        
        if lefttime is not None:
            # 验证预期寿命是否小于当前年龄
            if False:
                lefttime = None
            else:
                needModify += 1
                user.extrainfo.lefttime = lefttime
        
        if headuri is not None:
            needModify += 1
            user.extrainfo.headuri = headuri

        if bguri is not None:
            needModify += 1
            user.extrainfo.bguri = headuri

        if tags is not None:
            # 验证标签集是否合法
            if False:
                tags = None
            else:
                needModify += 1
                user.extrainfo.tags = tags

        if about_me is not None:
            needModify += 1
            user.extrainfo.about_me = about_me

        if needModify == 0: # 无变动
            db.session.rollback()
            return formattedResponse({}, 400, "extraintro passed is same as before!")
        else:
            db.session.commit()
            return formattedResponse({"extrainfo": user.extrainfo.to_json()})

        





        
