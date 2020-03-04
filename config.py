import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgres://adminUser:adminPass@localhost/postgres"