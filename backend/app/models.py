from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from flask import current_app, request, url_for
from . import db


class User(db.Model):
    '''用户数据表'''
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    sex = db.Column(db.Integer)
    location = db.Column(db.String(128))
    about_me = db.Column(db.Text())
    registration_time = db.Column(db.DateTime(), default=datetime.utcnow) # pass a func insted of a val
    last_logined = db.Column(db.DateTime(), default=datetime.utcnow) # pass a func instead of a val

    specialData = db.relationship("SpecialData", backref="owner", lazy="dynamic")
    texts = db.relationship("Text", backref="owner", lazy="dynamic")
    pictures = db.relationship("Picture", backref="owner", lazy="dynamic")

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def ping(self):
        '''update last_logined val'''
        self.last_logined = datetime.utcnow()
        db.session.add(self)

    def generate_auth_token(self, expiration=600):
        '''generate a auth token'''
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({"id": self.id}).decode("utf-8")

    @staticmethod
    def verify_auth_token(token):
        '''verify token is valid and return a user by token'''
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except SignatureExpired as e:
            return None # valid token, but expired
        except BadSignature as e:
            return None # invalid token
        user = User.query.get(data["id"])
        return user

    def to_json(self):
        json_user = {
            "uri": url_for("user", id=self.id),
            "username": self.username,
            "name": self.name,
            "sex": self.sex,
            "location": self.location,
            "about_me": self.about_me,
            "registration_time": self.registration_time,
            "last_logined": self.last_logined,
        }
        return json_user

    def __repr__(self):
        return "<User %r>" % self.username


class SpecialData(db.Model):
    '''个性数据'''
    __tablename__ = "specialDatas"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    headuri = db.Column(db.String(64))
    tags = db.Column(db.String(128))
    bguri = db.Column(db.String(64))

    def to_json(self):
        json_speData = {
            "id": self.id,
            "owner_id": self.owner_id,
            "headuri": self.headuri,
            "tags": self.tags,
            "bguri": self.bguri,
        }
        return json_speData

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

class Text(db.Model):
    '''文本表'''
    __tablename__ = "texts"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    strType = db.Column(db.Integer)
    tag = db.Column(db.String(64))
    createdTime = db.Column(db.DateTime(), default=datetime.utcnow)
    content = db.Column(db.String(64))

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

class Picture(db.Model):
    '''图片表'''
    __tablename__ = "pictures"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    uri = db.Column(db.String(64), unique=True)
    tag = db.Column(db.Integer)
    desc = db.Column(db.String(128), default="")

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
