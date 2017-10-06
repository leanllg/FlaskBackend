import json
import datetime
from flask import Blueprint, session, request, g, jsonify, abort
from flask_jwt_extended import JWTManager, jwt_refresh_token_required, jwt_required, create_access_token, create_refresh_token
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
    dic['avatar'] = '/home/default/default.jpg'
    user = User(name=dic['name'], password=pwd, phone=dic['phone'],\
    qq=dic['qq'], avatar=dic['avatar'])
    user.save()
    ret = {
        'access_token': create_access_token(identity=dic['name'], expires_delta=datetime.timedelta(days=180)),
        'refresh_token': create_refresh_token(identity=dic['name'] + dic['phone'], expires_delta=datetime.timedelta(hours=10))
    }
    return jsonify(ret), 200

@mode.route('/')

@mod.route('/<name>', method=['GET'])
@jwt_required
def 
