from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from ..models import User
from . import api

auth = HTTPBasicAuth()


def errorResponse(message, status_code):
    '''自定义错误响应函数'''
    response = jsonify({"error": "unauthorized", "message": message})
    response.status_code = status_code
    return response

@auth.verify_password
def verify_password(email, password):
    if email == "" or password == "":
        return False
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)

@auth.error_handler
def auth_error():
    return errorResponse("Invalid credentials", 403)

# @api.before_request
# @auth.login_required
# def before_request():
#     if not g.current_user:
#         return errorResponse("Not logined", 403)