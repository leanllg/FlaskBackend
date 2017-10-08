import json
import datetime
from flask import Blueprint, session, request, g, jsonify, abort
from flask_jwt_extended import JWTManager, jwt_refresh_token_required, jwt_required, create_access_token, create_refresh_token, get_raw_jwt
from main.models.user import User
from main.utils import get_salt_pwd
import bcrypt
from main.models import revoke_token
from main.models.TokenBlacklist import TokenBlacklist

mod = Blueprint('user', __name__, url_prefix='/api/user')

@mod.route('/<name>', methods=['POST'])
def signup(name):
	if not request.json:
		return jsonify({'status': 0}), 404
    user_info = User.query.filter_by(name=name).first()
    if user_info is not None:
        return jsonify({'status': 0, 'error': 'user exists'})
    password = request.json['password']
    pwd = get_salt_pwd(password)
    if not request.json['avatar']:
        avatar = '/home/default/default.jpg'
	else:
		avatar = request.json['avatar']
    user = User(name=name, password=pwd, phone=request.json['phone'],\
    qq=request.json['qq'], avatar=avatar, love_level=0)
    user.save()
    return jsonify({'status': 1}), 200

@mod.route('/<name>', method=['GET'])
def login(name):
    user_info = User.query.filter_by(name=name).first()
	if not request.json:
		return jsonify({'status': 0}), 404
    username = request.json.get('name', None)
    password = request.json.get('password', None)
    if username != user_info['name'] or not bcrypt.checkpw(password, user_info['password']):
        return jsonify({'status': 0, 'error': 'username or password wrong'}), 404
    dic = dict.copy(user_info)
    refresh_token = create_refresh_token(identity=dic, expires_delta=datetime.timedelta(hours=10))
    access_token = create_access_token(identity=dic, expires_delta=datetime.timedelta(days=180))
    add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
    add_token_to_database(refresh_token, app.config['JWT_IDENTITY_CLAIM'])
    ret = {
        'status': 1,
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return jsonify(ret), 200

@mod.route('/', methods=['DELETE'])
@jwt_refresh_token_required
def logout():
    current_user = get_jwt_identity()
    name = current_user['name']
    token = get_raw_jwt()
    try:
        revoke_token(token['jti'], current_user['name']);
        return jsonify({'status': 1}), 201
    except NoResultFound:
        return jsonify({'status': 0}), 404


@mod.route('/profile', methods=['POST'])
@jwt_required
def set_profile():
    current_user = get_jwt_identity()
    user_info = User.query.filter_by(name=current_user['name']).first()
    if user_info is None:
        return jsonify({'status': 0, 'error': 'no such user'}), 404
    name = request.json['name']
    qq = request.json['qq']
    phone = request.json['phone']
    if not name:
        user_info.name = name
    if not qq:
        user_info.qq = qq
    if not phone:
        user_info.phone = phone
    return jsonify(user_info.to_json()), 200

@mod.route('/profile', methods=['GET'])
def get_profile():
    current_user = get_jwt_identity()
    user_info = User.query.filter_by(name=current_user['name']).first()
    if user_info is None:
        return jsonify({'status': 0, 'error': 'no such user'}), 404
    return jsonify(user_info.to_json()), 200

@mod.route('/love_level', methods=['POST'])
@jwt_required
def love_level():
    current_user = get_jwt_identity()
    user_info = User.query.filter_by(name=current_user['name']).one()
    if request.json:
		if not request.json['love_level'] || request.json['love_level'] < 0
			return jsonify({'status': 0, 'error': 'love_level invalid'}), 402
        user_info.love_level = request.json['love_level']
        return jsonify({'status': 1}), 200
    return jsonify({'status': 0, 'error': 'not json'}), 404
