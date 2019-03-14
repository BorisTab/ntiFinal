# -*- coding: utf-8 -*-
from flask import request
from flask import Blueprint
from flask import render_template

from flask_mail import Message

from app.settings import DevConfig

from app.extensions import mail

from app.ar_server.models.forms.email_form import EmailForm


blueprint = Blueprint('landing', 'landing', template_folder='templates')


@blueprint.route('/send', methods=['POST'])
def send_email():
    pass


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    email_form = EmailForm(request.form)

    if request.method == 'POST':
        msg = Message(
            subject='Привет, дорогой друг!',
            sender=DevConfig.MAIL_USERNAME,
            recipients=[email_form.data['recipient_email']],
            body=email_form.data['message_text']
        )
        mail.send(msg)
    return render_template('index.html', form=email_form)


@blueprint.route('/en', methods=['GET'])
def index_eng():
    return render_template('index_eng.html')
