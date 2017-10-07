from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from main.models.case import Case
import datetime

case = Blueprint('case', __name__, url_prefix='/api/case')

@case.route('/all', methods=['GET'])
@jwt_required
def get_case():
    cases = User.query.all()
    now = datetime.datetime.now()
    now_stamp = now.timestamp()
    case_list = []
    for case in cases:
        case_time = case.time
        duration = case.duration
        if case_time + duration < now_stamp:
            case.status = 2
        dic = case.to_json()
        user = User.query.filter_by(id=case.user_id).one()
        other = User.query.filter_by(id=case.other_id).one()
        dic['user_name'] = user.name
        dic['other_name'] = other.name
        case_list.append(dic)
    return jsonify(case_list)

@case.route('/', methods=['POST'])
@jwt_required
def put_case():
    user = get_jwt_identity()
    name = user['name']
    user_info = User.query.filter_by(name=name).one()
    user_id = user_info.id
    if request.json:
        time = request.json['time']
        duration = request.json['duration']
        sex = request.json['sex']
        status = 1
        is_borrow = request.json['is_borrow']
        description = request.json['description']
        longtitude = request.json['longtitude']
        latitude = request.json['latitude']
        case = Case(user_id=user_id, time=time, is_borrow=is_borrow, status=status, \
        duration=duration, longtitude=longtitude, latitude=latitude, description=description, sex=sex)
        case.save()
        return jsonify({'status': 1}), 200

@case.route('/reception', methods=['POST'])
@jwt_required
def receive_case():
    other = get_jwt_identity()
    name = other['name']
    other_info = User.query.filter_by(name=name).one()
    other_id = other_info.id
    if request.json:
        user_name = request.json['user_name']
        case_id = request.json['id']
        case = Case.query.filter_by(id=case_id).one()
        case.status = 0
        case.other_id = other_id
        return jsonify({'status': 1}), 200
