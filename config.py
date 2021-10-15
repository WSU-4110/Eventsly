from logging import fatal
from os import environ, path

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'wsu4110eventsly!!'

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    DEVELOPMENT=True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:kiddobean19@localhost/eventsly'

class ProductionConfig(BaseConfig):
    DEBUG = False