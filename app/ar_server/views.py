from flask import Blueprint
from flask import render_template
from flask import request

from app.ar_server.models import ModelGatherer

blueprint = Blueprint('ar', 'ar', static_folder='../static')


@blueprint.route('/')
def main():
    return render_template('ar.html')


@blueprint.route('/get_model', methods=['POST'])
def get_model():
    max_lat = round(float(request.form['right-up-lat']), 2)
    max_lon = round(float(request.form['right-up-lng']), 2)
    min_lat = round(float(request.form['left-bottom-lat']), 2)
    min_lon = round(float(request.form['left-bottom-lng']), 2)

    gatherer = ModelGatherer()
    gatherer.get_model(max_lat, max_lon, min_lat, min_lon)
    return '200'
