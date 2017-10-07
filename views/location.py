from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.models.location import Location

location = Blueprint('location', __name__, url_prefix='/api/location')

@location.route('/', methods=['POST'])
@jwt_required
def put_loc():
    current_user = get_jwt_identity()
    if request.json:
        longtitude = request.json['longtitude']
        latitude = request.json['latitude']
        detail = request.json['detail']
        user = User.query.filter_by(name=current_user['name']).one()
        loc = Location(user_id=user.id, longtitude=longtitude, latitude=latitude, detail=detail)
        loc.save()
        return jsonify({'status': 1}), 201
    return jsonify({'status': 0, 'error': 'required json'})

@location.route('/', methods=['GET'])
@jwt_required
def get_loc():
    user = User.query.filter_by(name=get_jwt_identity()['name']).one()
    loc = Location.query.filter_by(user_id=user.id).one()
    return jsonify(loc.to_json())
