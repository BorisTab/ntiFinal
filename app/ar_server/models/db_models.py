# -*- coding: utf-8 -*-
from app.extensions import db


class Team(db.Model):
    __tablename__ = 'teams'

    name = db.Column(db.String, unique=True, primary_key=True)
    date_start = db.Column(db.DateTime)
    required_time = db.Column(db.Time)
    email = db.Column(db.String, unique=True)


class Quest(db.Model):
    __tablename__ = 'operations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)
    code = db.Column(db.String)

    # Use camelCase to friend Retrofit, SQLAlchemy and Glide
    thumbnailUrl = db.Column(db.String)


# ToDo: Add UserMixin
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    send_new = db.Column(db.Boolean, default=False)
    n_last = db.Column(db.Integer, default=0)
    files = db.relationship('MapFile', backref='users')
    is_authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, email, password):
        assert email is not None
        assert password is not None

        self.email = email
        self.password = password

    def is_authenticated(self):
        return self.is_authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.email)


class MapFile(db.Model):
    __tablename__ = 'models'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    obj_file = db.Column(db.LargeBinary)
    textures = db.Column(db.LargeBinary)
    thumbnail = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, obj_file, textures, thumbnail, user_id):
        self.name = name
        self.obj_file = obj_file
        self.textures = textures
        self.thumbnail = thumbnail
        self.user_id = user_id
