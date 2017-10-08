from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import get_jwt_identity, jwt_required
from PIL import Image
import os

img = Blueprint('img', __name__, url_prefix='/api/img')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    return '.'in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@img.route('/', methods=['POST'])
@jwt_required
def upload_img():
    user_info = get_jwt_identity()
    name = user_info['name']
    user = User.query.filter_by(name=name).one()
    path = os.path.join(app.config['UPLOAD_FOLDER'], name)
    if not os.path.exists(path):
        os.makedirs(path)
    file = request.files['avatar']
    size = (50, 50)
    im = Image.open(file)
    im.thumbnail(size)
    if file and allowed_file(file.filename):
        filename = file.filename
        avatar = os.path.join(path, filename)
        im.save(avatar)
        return jsonify({'status': 1, 'avatar': avatar}), 200
    return jsonify({'status': 0, 'error': 'not invlid file'}), 404

@img.route('/', methods=['GET'])
@jwt_required
def get_img():
    user_info = get_jwt_identity()
    name = user_info['name']
    user = User.query.filter_by(name=name).one()
    return send_file(user.avatar)
