from app.extensions import db


# ToDo: Add UserMixin
class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    files = db.relationship('MapFile', backref='users')

    def __init__(self, email, password):
        assert email is not None
        assert password is not None

        self.email = email
        self.password = password

    def is_authenticated(self):
        return True

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

    def __init__(self, name, obj_file, textures, thumbnail):
        self.name = name
        self.obj_file = obj_file
        self.textures = textures
        self.thumbnail = thumbnail
