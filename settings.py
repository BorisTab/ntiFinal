import os


class Config(object):
    """
    Base configuration
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./data/users.db'
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
