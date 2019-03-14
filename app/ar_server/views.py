#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import hashlib
import logging
import traceback

from os import getcwd
from time import strftime
from logging.handlers import RotatingFileHandler

from flask import session
from flask import jsonify
from flask import url_for
from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template

from pathlib import Path

import sqlalchemy.exc as sql_exc

from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import login_required

from flask_admin.contrib.sqla import ModelView

from app.constants import salt

from app.extensions import db

from app.extensions import admin
from app.extensions import login_manager

from app.ar_server.models.db_models import User
from app.ar_server.models.db_models import Quest
from app.ar_server.models.db_models import MapFile

from app.ar_server.models.file_waiter import FileWaiter
from app.ar_server.models.model_gatherer import ModelGatherer


from app.ar_server.models.forms.login_form import LoginForm
from app.ar_server.models.forms.map_creation_form import MapCreationForm
from app.ar_server.models.forms.registration_form import RegistrationForm


try:
    reload(sys)
    sys.setdefaultencoding('UTF8')
except NameError as e:
    print('>>>> Use linux btw')


handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
logger.addHandler(handler)


blueprint = Blueprint('ar', 'ar')
login_manager.login_view = '/ar/login'
admin.add_view(ModelView(Quest, db.session))


@blueprint.route('/quests', methods=['GET'])
def get_quests():
    all_quests = db.session.query(Quest).all()

    quests_response = []
    for i in range(len(all_quests)):
        quests_response.append({
            'id': all_quests[i].id,
            'name': all_quests[i].name,
            # ToDo: put code to Quest class
            'code': hashlib.md5(str(i).encode('utf-8')).hexdigest()[:8],
            'description': all_quests[i].description,
            'thumbnailUrl': all_quests[i].thumbnailUrl
        })
    return jsonify(quests_response)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.json:
        json = request.json

        user = db.session.query(User).filter_by(email=json['login']).first()
        try:
            if user.password == secure_password(json['password']):
                user.is_authenticated = True
                login_user(user)

                session.permanent = True
                db.session.commit()
                return '200'
        except AttributeError:
            return jsonify({'error': 'User with this login doesn\'t exist'})

    login_form = LoginForm(request.form)

    if current_user.is_authenticated:
        return redirect(url_for('ar.main'))
    elif request.method == 'POST':
        _login = login_form.data['email']
        password = login_form.data['password'].encode('utf-8')

        password = secure_password(password)

        # ToDo: add frontend validation
        if login_form.validate():
            user = db.session.query(User).filter_by(email=_login).first()

            # ToDo: get id and redirect to /ar/<int:id> after validation
            try:
                if user.password == password:
                    user.is_authenticated = True
                    login_user(user)

                    session.permanent = True
                    db.session.commit()
                    return redirect(url_for('ar.main', _id=user.id))
                else:
                    return jsonify({
                        'error': 'Invalid password'
                    }), 401
            except AttributeError:
                return jsonify({'error': 'Invalid login'})

    return render_template('login.html', form=login_form)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.json:
        json = request.json

        try:
            new_user = User(json['login'], secure_password(json['password']))
            new_user.is_authenticated = True
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            session.permanent = True
        except sql_exc.IntegrityError:
            return jsonify({
                'error': 'User with this login exists'
            }), 400
        return '200'

    register_form = RegistrationForm(request.form)

    if current_user.is_authenticated:
        return redirect(url_for('ar.main'))

    elif request.method == 'POST':
        form_login = register_form.data['email']
        form_password = register_form.data['password'].encode('utf-8')

        # ToDo: add frontend validation
        # ToDo: redirect to /ar/<int:id> where id - new user id
        # Stepic, vk ... uses same pattern
        if register_form.validate():
            try:
                new_user = User(form_login, secure_password(form_password))
                new_user.is_authenticated = True
                db.session.add(new_user)
                db.session.commit()

                login_user(new_user)

                session.permanent = True
                return redirect(url_for('ar.main', _id=new_user.id))
            except sql_exc.IntegrityError:
                return jsonify({
                    'error': 'User with this login exists'
                }), 400
    return render_template('register.html', form=register_form)


@blueprint.route('/logout')
@login_required
def logout():
    user = current_user
    user.is_authenticated = False
    logout_user()
    db.session.commit()
    return redirect(url_for('ar.login'))


@login_manager.user_loader
def load_user(_login):
    return User.query.filter_by(email=_login).first()


@blueprint.route('/<int:_id>', methods=['GET', 'POST'])
@blueprint.route('/', methods=['GET'])
@login_required
def main(_id=''):
    form = MapCreationForm(request.form)

    if request.method == 'POST':

        if form.validate():
            name = form.data['map_name']
            max_lat = round(float(request.form['right_up_lat']), 2)
            max_lon = round(float(request.form['right_up_lng']), 2)
            min_lat = round(float(request.form['left_bottom_lat']), 2)
            min_lon = round(float(request.form['left_bottom_lng']), 2)

            ModelGatherer.get_model(max_lat, max_lon, min_lat, min_lon)

            # ToDo: simplify? -> Create additional class
            obj_file = generate_file_path('map_.obj')
            mtl_file = generate_file_path('map_.mtl')
            thumbnail = generate_file_path('map_.jpg')

            FileWaiter(obj_file).wait()
            FileWaiter(mtl_file).wait()
            FileWaiter(thumbnail).wait()

            with open(obj_file, 'rb') as file:
                obj_file = file.read()
            with open(thumbnail, 'rb') as file:
                thumbnail = file.read()
            with open(mtl_file, 'rb') as file:
                mtl_file = file.read()

            try:
                new_map = MapFile(name, obj_file, mtl_file, thumbnail, _id)
                db.session.add(new_map)
            except sql_exc.IntegrityError:
                return jsonify({
                    'error': 'Map with given name is exist'
                }), 409

            user = db.session.query(User).filter_by(id=_id).first()
            user.send_new = True
            user.n_last += 1
            db.session.commit()

            return redirect(url_for('ar.main', _id=user.id))  # '', 204 опа ф5

    models = db.session.query(MapFile).filter_by(user_id=_id).all()
    if len(models) == 0:
        models = None
    return render_template('ar.html', form=form, models=models)


@blueprint.route('/status/<int:_id>', methods=['GET'])
def status(_id):
    user = db.session.query(User).filter_by(id=_id).first()

    map_files = []
    rows = db.session.query(MapFile).order_by(MapFile.id.desc()).limit(user.n_last).all()

    for i in range(user.n_last):
        map_files.append([
            str(rows[i].obj_file, 'utf-8'),
            str(rows[i].textures, 'utf-8'),
            str(rows[i].thumbnail)
            # base64.b64encode()
        ])

    user.n_last = 0
    db.session.commit()

    files = {x: y for x, y in enumerate(map_files)}
    return jsonify(files)


def secure_password(pwd):
    return str(hashlib.sha256((str(pwd) + str(salt)).encode('utf-8')).hexdigest())


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


def generate_file_path(name):
    return Path(getcwd() + '/app/ar_server/' + name).as_posix()


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
