from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from flask import current_app, request, url_for
from . import db

# sqlalchemy库中声明了orm支持的列类型
# 可以通过sqlalchemy的实例db来使用(这是一种方式)

# 文档资料
# https://xintiaohuiyi.gitbook.io/flask-note/4flaskshu-ju-ku/58-duo-dui-duo-guan-xi-shi-xian

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    sex = db.Column(db.Integer, nullable=False) # 0是女性，1是男性
    location = db.Column(db.String(128), default="四川-成都")

    register_time = db.Column(db.DateTime(),
                              default=datetime.utcnow, nullable=False)
    last_logined = db.Column(db.DateTime(),
                             default=datetime.utcnow, nullable=False)

    extrainfo = db.relationship("ExtraInfo", uselist=False)
    records = db.relationship("Record", backref="user", lazy="dynamic")
    pictures = db.relationship("Picture", backref="user", lazy="dynamic")

    def __init__(self, *args, **kw):
        pass

    def __repr__(self):
        return "<<User: %r>>" % self.to_json()

    def to_json(self):
        '''transform'''
        return {
            "user_id": self.user_id,
            "telephone": self.telephone,
            "username": self.username,
            "sex": self.sex,
            "location": self.location,
            "extrainfo": self.extrainfo.to_json(),
        }

class ExtraInfo(db.Model):
    __tablename__ = "extrainfos"

    info_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    birth = db.Column(db.Integer)
    lefttime = db.Column(db.Integer, default=77)
    headuri = db.Column(db.String(128), default="")
    bguri = db.Column(db.String(128), default="")
    tags = db.Column(db.String(128), default="")
    about_me = db.Column(db.String(512), default="")
    user = db.relationship("User", uselist=False)

    def __init__(self, *args, **kw):
        pass

    def __repr__(self):
        # %r used in repr is right
        return "<<ExtraInfo: %r>>" % self.to_json()

    def to_json(self):
        '''transform'''
        return {
            "info_id": self.info_id,
            "user_id": self.user_id,
            "age": self.age,
            "birth": self.birth,
            "lefttime": self.lefttime,
            "headuri": self.headuri,
            "bguri": self.bguri,
            "tags": self.tags,
            "register_time": self.register_time,
            "last_logined": self.last_logined,
        }

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def updateSomeWhenLogin(self):
        self.last_logined = datetime.utcnow()
        db.session.add(self)

    def generate_auth_token(self, expiration=600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"user_id": self.user_id})

    def verify_auth_token(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except SignatureExpired as e:
            return None # valid token, but expired
        except BadSignature as e:
            return None # invalid token
        user = User.query.get(data["user_id"])
        return user


class Record(db.Model):
    __tablename__ = "records"

    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    create_time = db.Column(db.DateTime(), default=datetime.utcnow)
    where = db.Column(db.String(256), default="")
    content = db.Column(db.String(256), default="")
    texturi = db.Column(db.String(128), default="")
    pic_uri = db.Column(db.String(128), default="")
    tags = db.Column(db.String(128), default="")

    def __init__(self, *args, **kw):
        pass

    def __repr__(self):
        return "<<Record: %r>>" % self.to_json()

    def to_json(self):
        '''transform'''
        return {
            "record_id": self.record_id,
            "user_id": self.user_id,
            "create_time": self.create_time,
            "content": self.content,
            "texturi": self.texturi,
            "pic_uri": self.pic_uri,
            "tags": self.tags,
        }

class Picture(db.Model):
    __tablename__ = "pictures"

    pic_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    create_time = db.Column(db.DateTime(), default=datetime.utcnow)
    uri = db.Column(db.String(128), default="")
    tags = db.Column(db.String(128), default="")

    def __init__(self, *args, **kw):
        pass


