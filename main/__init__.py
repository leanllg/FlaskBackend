from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__, instance_relative_config=True)
jwt = JWTManager()

from main.views.cases import case
from main.views.img import img
from main.views.location import location
from main.views.token import token
from main.views.user import mod

from main.models import db, is_token_revoked

def create_app():
    app.config.from_object('config')
    app.config.from_pyfile('config.py')

    db.init_app(app)
    jwt.init_app(app)

    @app.before_first_request
    def setup_sqlalchemy():
        db.create_all()

    from main.tokenerror import expired_token, invalid_token, revoked_token

    @jwt.token_in_blacklist_loader
    def check_if_token_revoked(decoded_token):
        return is_token_revoked(decoded_token)

    app.register_blueprint(case)
    app.register_blueprint(img)
    app.register_blueprint(location)
    app.register_blueprint(token)
    app.register_blueprint(mod)

    return app
