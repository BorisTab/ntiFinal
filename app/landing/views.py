# -*- coding: utf-8 -*-
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


blueprint = Blueprint('landing', 'landing', static_folder='static', template_folder='templates')


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


@blueprint.route('/app/download')
def download_app():
    return send_from_directory(blueprint.static_folder, 'app/app.apk')


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = Message(
            subject='Привет, дорогой друг!',
            sender=DevConfig.MAIL_USERNAME,
            recipients=[request.form['email']],
            body='Привет!!'
        )
        mail.send(msg)

        try:
            if db.session.query(Team).filter_by(date_start=request.form['data-input']).all() == 7:
                return jsonify({'error': 'mesta zanyati'})
            else:
                new_team = Team(
                    name=request.form['name'],
                    date_start=request.form['data-input'],
                    email=request.form['email']
                )

                db.session.add(new_team)
                db.session.commit()
                return jsonify({'status': '200'})
        except (sql_exc.IntegrityError, TypeError):
            return jsonify({'error': 'sql error'})

    return render_template('index.html')


@blueprint.route('/en', methods=['GET'])
def index_eng():
    return render_template('index_eng.html')
