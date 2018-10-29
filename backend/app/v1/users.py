from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, SpecialData

@api.route("/users/<int:userid>")
def get_user(userid):
    user = User.query.get_or_404(userid) # 主键查询
    return jsonify(user.to_json())

