# -*- coding: utf-8 -*-
import hashlib
import pyqrcode

from flask import jsonify
from flask import request
from flask import Blueprint
from flask import render_template
from flask import send_from_directory

import sqlalchemy.exc as sql_exc
from flask_mail import Message

from app.settings import DevConfig

from app.extensions import db
from app.extensions import mail

from app.ar_server.models.db_models import Team

from pathlib import Path
from os import getcwd
from os import path
from os import rename
import shutil


a = Path(getcwd()).parents[0].as_posix()
blueprint = Blueprint('landing', 'landing', static_folder=path.join(a, 'static'))
print(path.join(a, '/static'))


schedule = {
  'пн': ['8:00', '10:00', '12:00', '14:00'],
  'вт': ['8:00', '10:00', '12:00', '14:00'],
  'ср': ['8:00', '10:00', '12:00', '14:00'],
  'чт': ['8:00', '10:00', '12:00', '14:00'],
  'пт': ['8:00', '10:00', '12:00', '14:00'],
  'сб': ['8:00', '10:00', '12:00', '14:00'],
  'вс': ['8:00', '10:00', '12:00', '14:00']
}

busy_box = [
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0]
]


@blueprint.route('/test', methods=['GET', "POST"])
def test():
    return render_template('test.html')


@blueprint.route('/route/draw', methods=['GET', "POST"])
def draw_group_route():
    if request.method == 'POST':
        json = request.json

        n_teams = json['amount']
        group_id = json['team_code']
        return jsonify({'n': n_teams, 'id': group_id})
    else:
        return render_template('route.html')


@blueprint.route('/app/download')
def download_app():
    return send_from_directory(blueprint.static_folder, 'app/app.apk')


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        try:
            '''
            if len(db.session.query(Team).filter_by(dateStart=request.form['data-input']).all()) == 7:
                return jsonify({'error': 'mesta zanyati'})
            else:
            '''
            new_team = Team(
                name=request.form['name'],
                # dateStart=request.form['data-input'],
                email=request.form['email'],
            )

            new_team.code = hashlib.md5(str(new_team.id).encode('utf-8')).hexdigest()[:8]

            data = pyqrcode.create('nti://' + new_team.code)
            data.png('qr_code.png', scale=6)
            # 6adf97f8
            shutil.move(
                Path(getcwd()).as_posix() + '/qr_code.png',
                Path(getcwd()).as_posix() + '/app/static/qr_code.png'
            )

            msg = Message(
                subject='Привет, дорогой друг!',
                sender=DevConfig.MAIL_USERNAME,
                recipients=[request.form['email']],
            )
            msg.html = render_template('email.html', code=new_team.code)
            # render_template('email.html', code=new_team.code)

            mail.send(msg)

            db.session.add(new_team)
            db.session.commit()
            return jsonify({'status': '200'})
        except (sql_exc.IntegrityError, TypeError) as e:
            print(e.args)
            return jsonify({'error': 'sql error'})

    return render_template('index.html')


@blueprint.route('/en', methods=['GET'])
def index_eng():
    return render_template('index_eng.html')
