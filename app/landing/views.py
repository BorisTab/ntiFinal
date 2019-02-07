from flask import Blueprint
from flask import render_template


blueprint = Blueprint('landing', 'landing')


@blueprint.route('/', methods=['GET'])
def main():
    return render_template('index.html')
