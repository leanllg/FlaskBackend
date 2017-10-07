from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from main.models.case import Case
from main.models import db
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
            db.session.delete(case)
        else:
            dic = case.to_json()
            user = User.query.filter_by(id=case.user_id).one()
            other = User.query.filter_by(id=case.other_id).one()
            dic['user_name'] = user.name
            dic['other_name'] = other.name
            case_list.append(dic)
    db.commit()
    return jsonify(case_list)


@case.route('/')
