import json
from flask import Blueprint, session, request, g, jsonify, abort
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from main.models.user import User
from main.utils import get_salt_pwd

mod = Blueprint('user', __name__, url_prefix='/api/user')


@mod.route('/<name>', method=['POST'])
def signup(name):
    user_info = User.query.filter_by(name=name).first()
    if user_info is not None:
        return jsonify({'status': 0, 'error': 'user exists'})
    _json = request.get_data()
    dic = json.loads(_json)
    password = dic['password']
    pwd = get_salt_pwd(password)
