from os import path
from os import pardir
from os import getcwd
from os import environ

from pathlib import Path


class Config(object):
    """
    Base configuration
    """
    SECRET_KEY = environ.get('SECRET_KEY', 'secret-key')
    APP_DIR = path.abspath(path.dirname(__file__))
    PROJECT_ROOT = path.abspath(path.join(APP_DIR, pardir))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + Path(getcwd() + '/app/data/users.db').as_posix()
    TESTING = False


class ProductionConfig(Config):
    """
    Production configuration
    """
    ENV = 'production'
    DB_NAME = 'users'
    DEBUG = False


class DevConfig(Config):
    """
    Development configuration
    """
    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'dev'
