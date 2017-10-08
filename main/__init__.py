from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__, instance_relative_config=True)
jwt = JWTManager(app)

app.config.from_object('config')
app.config.from_pyfile('config.py')

from main.views.cases import case
from main.views.img import img
from main.views.location import location
from main.views.token import token
from main.views.user import mod
app.register_blueprint(case)
app.register_blueprint(img)
app.register_blueprint(location)
app.register_blueprint(token)
app.register_blueprint(mod)
