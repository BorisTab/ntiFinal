from flask import Flask

from settings import DevConfig

from app.landing import views as landing_views
from app.ar_server import views as ar_views


def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    pass


def register_blueprints(app):
    app.register_blueprint(ar_views.blueprint, url_prefix='/ar')
    app.register_blueprint(landing_views.blueprint, url_prefix='/')
