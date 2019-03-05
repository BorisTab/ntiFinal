# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import render_template


blueprint = Blueprint('landing', 'landing', template_folder='templates')


@blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@blueprint.route('/en', methods=['GET'])
def index_eng():
    return render_template('index_eng.html')
