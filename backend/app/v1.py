from flask import Flask, abort, url_for, request, jsonify
from flask_restful import Api, Resource, reqparse
from .models import User, SpecialData
import functools

class UserListAPI(Resource):
    uri = "/api/v1/users"
    endpoint = "userlist"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def get(self):
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
        self

class UserAPI(Resource):
    uri = "/api/v1/user/<int:id>"
    endpoint = "user"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def get(self, id):
        user = User.query.filter_by(id=id).first_or_404()
        return jsonify({"user": user.to_json()})

    def put(self, id):
        pass
