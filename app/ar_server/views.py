#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import hashlib
import logging
import traceback

from os import getcwd
from time import strftime
from threading import Thread
from logging.handlers import RotatingFileHandler

from flask import abort
from flask import jsonify
from flask import url_for
from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template

from pathlib import Path
# from requests import

from app.constants import salt

from app.extensions import db
from app.extensions import login_user
from app.extensions import logout_user
from app.extensions import current_user
from app.extensions import login_manager
from app.extensions import login_required

from app.ar_server.models.db_models import Users
from app.ar_server.models.db_models import MapFile

from app.ar_server.models.file_waiter import FileWaiter
from app.ar_server.models.asset_sender import AssetSender
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


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)

    if current_user.is_authenticated:
        return redirect(url_for('ar.main'))
    elif request.method == 'POST':
        _login = login_form.data['email']
        password = login_form.data['password'].encode('utf-8')

        password = hashlib.sha256(password + salt).hexdigest()

        # ToDo: add frontend validation
        if login_form.validate():
            user = db.session.query(Users).filter_by(email=_login, password=password).first()

            # ToDo: get id and redirect to /ar/<int:id> after validation
            try:
                if user.password == password:
                    user.authenticated = True
                    login_user(user)
                    # _next = request.args.get('next')

                    db.session.commit()
                    return redirect(url_for('ar.main', _id=user.id))
            except Exception as exception:
                print(exception.args)
                return abort(401)

    return render_template('login.html', form=login_form)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
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
                new_user = Users(form_login, hashlib.sha256(form_password + salt).hexdigest())
                new_user.authenticated = True
                db.session.add(new_user)
                db.session.commit()

                login_user(new_user)

                return redirect(url_for('ar.main', _id=new_user.id))
            except Exception as exception:
                print(exception.args)
                # ToDo: user exists
                return abort(401)
    return render_template('register.html', form=register_form)


@blueprint.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    logout_user()
    db.session.commit()
    return redirect(url_for('ar.login'))


@login_manager.user_loader
def load_user(_login):
    return Users.query.filter_by(email=_login).first()


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

            new_map = MapFile(name, obj_file, mtl_file, thumbnail, _id)
            db.session.add(new_map)

            user = db.session.query(Users).filter_by(id=_id).first()
            user.send_new = True
            user.n_last += 1
            db.session.commit()

            return redirect(url_for('ar.main', _id=user.id))  # '', 204 опа ф5

    models = db.session.query(MapFile).filter_by(user_id=_id).all()
    if len(models) == 0:
        models = None
    return render_template('ar.html', form=form, models=models)


class Building(object):

    def __init__(self, obj, mtl, jpg):
        self.obj = obj
        self.mtl = mtl
        self.jpg = jpg


@blueprint.route('/status/<int:_id>', methods=['GET'])
def status(_id):
    user = db.session.query(Users).filter_by(id=_id).first()

    map_files = []
    rows = db.session.query(MapFile).order_by(MapFile.id.desc()).limit(user.n_last).all()
    # rows = rows[::-1]

    for i in range(user.n_last):
        map_files.append([
            str(rows[i].obj_file),
            str(rows[i].textures),
            str(rows[i].thumbnail)
        ])

    user.n_last = 0
    db.session.commit()

    files = {x: y for x, y in enumerate(map_files)}
    return jsonify(files)


def collect_files():
    files = [
        open('map_.obj').read(),
        open('map_.mtl').read(),
        open('map_.jpg').read(),
    ]
    return files


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


########################
#        DANGER        #
#     DEBUG USE ONLY   #
########################


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
