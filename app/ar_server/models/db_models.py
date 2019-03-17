# -*- coding: utf-8 -*-
from app.extensions import db


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, autoincrement=True)
    name = db.Column(db.String, unique=True)
    # dateStart = db.Column(db.String)
    email = db.Column(db.String, unique=True, primary_key=True)
    code = db.Column(db.String)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    position = db.Column(db.String)
    teamCode = db.Column(db.Integer, db.ForeignKey('teams.code'))
