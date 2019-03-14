from wtforms import Form
from wtforms import validators
from wtforms import StringField
from wtforms import SubmitField


class EmailForm(Form):
    recipient_name = StringField('Имя', [
        validators.DataRequired()
    ])
    recipient_email = StringField('', [
        validators.DataRequired(),
        validators.email,
        validators.Length(min=4, max=25)
    ])
    message_text = StringField('Сообщение', [
        validators.DataRequired(),
    ])
    button = SubmitField('Отправить')
