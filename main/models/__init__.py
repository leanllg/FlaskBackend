from flask.ext.sqlalchemy import SQLALchemy
from main import app
from datetime import datetime

db = SQLALchemy(app)

from main.models import case
from main.models import location
from main.models import user
from main.models import TokenBlacklist
from flask_jwt_extended import decode_token

def _timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp)

def add_token_to_database(encoded_token, identity):
    decoded_token = decode_token(encoded_token)
    db_token = TokenBlacklist(
        jti=decoded_token['jti'],
        token_type=decoded_token['token_type'],
        user_identity=decoded_token['user_identity'],
        expires=decoded_token['expires'],
        revoked=decoded_token['revoked']
    )
    db_token.save()

def get_user_tokens(user_identity):
    return TokenBlacklist.query.filter_by(user_identity=user_identity).all()


def revoke_token(jti, user):
    try:
        token = TokenBlacklist.query.filter_by(jti=jti, user_identity=user).one()
        token.revoked = True
        db.session.commit()
    except NoResultFound:
        raise TokenNotFound("Could not find the token {}".format(token_id))


def unrevoke_token(token_id, user):
    try:
        token = TokenBlacklist.query.filter_by(id=token_id, user_identity=user).one()
        token.revoked = False
        db.session.commit()
    except NoResultFound:
        raise TokenNotFound("Could not find the token {}".format(token_id))


def prune_database():
    now = datetime.now()
    expired = TokenBlacklist.query.filter(TokenBlacklist.expires < now).all()
    for token in expired:
        db.session.delete(token)
    db.session.commit()
