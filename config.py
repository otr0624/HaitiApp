import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'qwerty'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    """Development-environment-specific config class"""
    SECRET_KEY = 'qwerty'
    DATABASE_FILENAME = os.path.join(basedir, 'development_database.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILENAME
    DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production-environment-specific config class"""
    SECRET_KEY = os.environ.get('SECRET_KEY')
