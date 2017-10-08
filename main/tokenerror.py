from main import jwt

@jwt.expired_token_loader
def expired_token():
    return jsonify({
        'status': 0,
        'error': 'token expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token():
    return jsonify({
        'status': 0,
        'error': 'token invalid'
    }), 401

@jwt.revoked_token_loader
def revoked_token():
    return jsonify({
        'status': 0,
        'error': 'token revoked'
    }), 401
