import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'qwerty'
    SQLALCHEMY_DATABASE_URI = os.environ.get('CLEARDB_DATABASE_URL') or 'mysql+pymysql://root:qwerty@localhost/hca_data'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    TESTING = False


class DevelopmentConfig(BaseConfig):
    """Development-environment-specific config class"""
    SECRET_KEY = 'qwerty'
    DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production-environment-specific config class"""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False
    TESTING = False
