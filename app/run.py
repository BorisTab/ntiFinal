# -*- coding: utf-8 -*-
from flask import Flask

from settings import DevConfig

from app.extensions import db
from app.extensions import login_manager

from app.ar_server import views as ar_views
from app.landing import views as landing_views
from app.science_art import views as sciart_views


def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)

    print(app.url_map)
    return app


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    app.register_blueprint(ar_views.blueprint, url_prefix='/ar')
    app.register_blueprint(landing_views.blueprint, url_prefix='/')
    app.register_blueprint(sciart_views.blueprint, url_prefix='/sciart')
