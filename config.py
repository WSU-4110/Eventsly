from logging import fatal
from os import environ, path

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'wsu4110eventsly!!'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    DEVELOPMENT=True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:kiddobean19@localhost/eventsly'

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://tedlxxnccqarfg:c7a414983644bb4eca43b0d2465cb2b62d283433d18f097efd97f47b3788a275@ec2-44-198-29-193.compute-1.amazonaws.com:5432/db31eh5kiorqfk'