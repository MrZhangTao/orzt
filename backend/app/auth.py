from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from .models import User, PowerType

auth = HTTPBasicAuth()


def errorResponse(message, status_code):
    '''自定义错误响应函数'''
    response = jsonify({"error": "unauthorized", "message": message})
    response.status_code = status_code
    return response

# 注册验证函数，用于auth的login_required装饰器
@auth.verify_password
def verify_password(phone_or_token, password):
    if phone_or_token == "":
        return False
    # first try to authenticate by token
    user = User.analyse_auth_token(phone_or_token)
    if not user:
        # try to authenticate with telephone/password
        user = User.query.filter_by(telephone=phone_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user # save user to the app context--g
    return True

# 注册错误处理回调
@auth.error_handler
def auth_error():
    return errorResponse("Unauthorized Access", 401)

def isAdministration(user):
    if user.power == PowerType.Administration:
        return True
    else:
        return False


