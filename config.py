import os


class BaseConfig(object):
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'qwerty'
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
