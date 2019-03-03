from wtforms import Form
from wtforms import validators
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField


class LoginForm(Form):
    email = StringField('Email Address', [
        validators.DataRequired(),
        validators.Length(min=4, max=25)
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=6, max=30)
    ])
    button = SubmitField('Войти')
