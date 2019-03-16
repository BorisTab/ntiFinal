# -*- coding: utf-8 -*-
from os import path
from os import pardir
from os import getcwd
from os import environ

from datetime import timedelta

from pathlib import Path


class Config(object):
    """
    Base configuration
    """
    SECRET_KEY = environ.get('SECRET_KEY', 'secret-key')
    APP_DIR = path.abspath(path.dirname(__file__))
    PROJECT_ROOT = path.abspath(path.join(APP_DIR, pardir))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + Path(getcwd() + '/app/data/data.db').as_posix()
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
    TESTING = False

    # SMTP server config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'mail@xnoobs.ru'
    MAIL_PASSWORD = 'g=&SZy9e\''


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
