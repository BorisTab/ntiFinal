from flask import request
from flask import Blueprint
from flask import render_template

from app.ar_server.models.model_gatherer import ModelGatherer
from app.ar_server.models.asset_loader import AssetLoader


blueprint = Blueprint('ar', 'ar')


@blueprint.route('/', methods=['GET'])
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

    loader = AssetLoader()
    loader.send_object()
    return '200'
