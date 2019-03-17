#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import logging
import traceback

from time import strftime
from logging.handlers import RotatingFileHandler

from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask import request

from app.extensions import db

from app.ar_server.models.db_models import Team
from app.ar_server.models.db_models import User


# Reload default encoding for linux distros
try:
    reload(sys)
    sys.setdefaultencoding('UTF8')
except NameError as e:
    # Exception catches if os -> 'nt'
    print('>>>> Use linux btw')


# Add logger for application
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
logger.addHandler(handler)

# Create blueprint for /ar views
blueprint = Blueprint('ar', 'ar', static_folder='../static')


@blueprint.route('/user/update/map', methods=['GET', "POST"])
def update_map():
    """ update map """
    return render_template('map.html')


@blueprint.route('/user/update/position', methods=['POST'])
def update_user_position():
    """ update position of user """

    json = request.json

    user = db.session.query(User).filter_by(id=json['id']).first()
    user.position = json['position']

    db.session.add(user)
    db.session.commit()

    return jsonify(request.json())


@blueprint.route('/user/set/code', methods=['POST'])
def set_team_code():
    """ set team code """

    json = request.json

    user = db.session.query(User).filter_by(id=json['id']).first()
    user.teamCode = json['teamCode']
    db.session.commit()
    return '200'


@blueprint.route('/user/set/id', methods=['GET'])
def set_user_id():
    """ register new user when android app launched first time """

    new_user = User()
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id})


@blueprint.route('/team/get/amount', methods=['POST'])
def get_team_count():
    """ returns amount of teams """
    return jsonify({'amount': len(db.session.query(Team).all())})


@blueprint.after_request
def after_request(response):
    """ Logging after every request. """
    # This avoids the duplication of registry in the log,
    # since that 500 is already logged via @app.errorhandler.
    if response.status_code != 500:
        ts = strftime('[%Y-%b-%d %H:%M]')
        logger.error(
            '%s %s %s %s %s %s',
            ts,
            request.remote_addr,
            request.method,
            request.scheme,
            request.full_path,
            response.status
        )
    return response


@blueprint.errorhandler(Exception)
def exceptions():
    """ Logging after every Exception. """
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    logger.error(
        '%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
        ts,
        request.remote_addr,
        request.method,
        request.scheme,
        request.full_path,
        tb
    )
    return "Internal Server Error", 500


###########################
#         DANGER          #
#      DEBUG USE ONLY     #
# NEVER USE IN PRODUCTION #
###########################


@blueprint.route('/create')
def create_db():
    db.create_all()
    db.session.commit()
    return '200'


@blueprint.route('/drop')
def drop_db():
    db.drop_all()
    db.session.commit()
    return '200'
