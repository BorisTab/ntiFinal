# -*- coding: utf-8 -*-
from flask_login import LoginManager
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import login_required

from flask_sqlalchemy import SQLAlchemy


login_manager = LoginManager()
db = SQLAlchemy()
