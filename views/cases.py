from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from main.models.case import case

case = Blueprint('case', __name__, url_prefix='/api/case')

@case.route('/all', methods=['GET'])
@jwt_required
def put_case():
    
