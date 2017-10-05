from flask import jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

@jwt.expired_token_loader
def expired_token():
    return jsonify({
        'status': 0,
        'error': 'the token has expired'
    }), 200
