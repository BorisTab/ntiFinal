# -*- coding: utf-8 -*-
from wtforms import Form
from wtforms import validators
from wtforms import SubmitField
from wtforms import StringField
from wtforms import PasswordField


class RegistrationForm(Form):
    email = StringField('Email Address', [
        validators.Length(min=6, max=35)
    ])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    button = SubmitField('Регистрация')
