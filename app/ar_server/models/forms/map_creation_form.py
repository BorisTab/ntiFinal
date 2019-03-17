#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from wtforms import Form
from wtforms import validators
from wtforms import StringField
from wtforms import SubmitField


class MapCreationForm(Form):
    right_up_lat = StringField('', [
        validators.DataRequired()
    ])
    right_up_lng = StringField('', [
        validators.DataRequired()
    ])
    left_bottom_lat = StringField('', [
        validators.DataRequired()
    ])
    left_bottom_lng = StringField('', [
        validators.DataRequired()
    ])

    right_up = StringField('широта;долгота', [
        validators.DataRequired()
    ])
    left_bottom = StringField('широта;долгота', [
        validators.DataRequired()
    ])

    map_name = StringField('Введите имя модели', [
        validators.DataRequired()
    ])

    form_button = SubmitField('Отправить')
