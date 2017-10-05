from flask.ext.sqlalchemy import SQLALchemy
from main import app
from flask.ext.httpauth import HTTPBasicAuth, HTTPTokenAuth


db = SQLALchemy(app)

from main.models import case
from main.models import location
from main.models import user

def set_user_info():
