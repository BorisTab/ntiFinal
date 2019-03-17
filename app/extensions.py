# -*- coding: utf-8 -*-
from flask_admin import Admin
from flask_mail import Mail
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


mail = Mail()
admin = Admin()
db = SQLAlchemy()
login_manager = LoginManager()
