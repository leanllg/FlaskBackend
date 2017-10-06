from flask_jwt_extended import create_access_token, jwt_refresh_token_required, get_jwt_identity
from flask import Blueprint

token = Blueprint('token', __name__, url_prefix='/api/token')

@token.route('/refresh', methods=['GET'])
@jwt_refresh_token_required
def refresh_token():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
    return jsonify({'status': 1, 'access_token': access_token}), 201
