# -*- coding: utf-8 -*-
from app.extensions import db


# ToDo: Add UserMixin
class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    send_new = db.Column(db.Boolean, default=False)
    n_last = db.Column(db.Integer, default=0)
    files = db.relationship('MapFile', backref='users')
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, email, password):
        assert email is not None
        assert password is not None

        self.email = email
        self.password = password

    def is_authenticated(self):
        return self.authenticated

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
