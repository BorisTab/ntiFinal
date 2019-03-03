from wtforms import Form
from wtforms import validators
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField


class LoginForm(Form):
    email = StringField('Email Address', [
        validators.DataRequired()
    ])
    password = PasswordField('Password', [
        validators.DataRequired()
    ])
    button = SubmitField('Войти')
