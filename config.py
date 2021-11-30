from logging import fatal
from os import environ, path

class BaseConfig(object):
    DEBUG = True
    SECRET_KEY = 'wsu4110eventsly!!'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

class TestingConfig(BaseConfig):
    TESTING = True
    localpass =''
    try:
        with open('dbconfig.txt') as f:
            localpass = f.readline()
    except FileNotFoundError:
        pass

    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:{localpass}@localhost/eventslytest'

class TestingConfig(BaseConfig):
    TESTING = True
    localpass =''
    try:
        with open('dbconfig.txt') as f:
            localpass = f.readline()
    except FileNotFoundError:
        pass

    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:{localpass}@localhost/eventslytest'

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DEVELOPMENT=True
    localpass = ''

    # set localdb password in dbconfig.txt
    # dbconfig.txt is on .gitignore so that we can leave this file alone when we flask run
    try:
        with open('dbconfig.txt') as f:
            localpass = f.readline()
    except FileNotFoundError:
        pass

    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:{localpass}@localhost/eventsly'

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://tedlxxnccqarfg:c7a414983644bb4eca43b0d2465cb2b62d283433d18f097efd97f47b3788a275@ec2-44-198-29-193.compute-1.amazonaws.com:5432/db31eh5kiorqfk'