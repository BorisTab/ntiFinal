from flask import Blueprint
from flask import render_template


blueprint = Blueprint('landing', 'landing', static_folder='../static')


@blueprint.route('/demo', methods=['GET'])
def send_mail():
    return render_template('science-art.html')


@blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')
