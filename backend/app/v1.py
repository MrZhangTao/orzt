from flask import Flask, abort, url_for, request, jsonify, g, current_app, make_response
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask_restful import Api, Resource, reqparse
from .models import User
import functools
from .auth import auth
from . import db
from datetime import datetime

operaTypeEnums = ["lt", "rt"]


class Users(Resource):
    uri = "/api/v1/users"
    endpoint = "/api/v1/users"
    decorators = [auth.login_required]
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def get(self):
        pass
    
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
