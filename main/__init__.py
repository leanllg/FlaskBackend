from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__, instance_relative_config=True)
jwt = JWTManager(app)

app.config.from_object('config')
app.config.from_pyfile('config.py')
