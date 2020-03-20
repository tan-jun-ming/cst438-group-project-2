import utils

class Config(object):
    SQLALCHEMY_DATABASE_URI = utils.get_database_uri()
    _jwt_secret = utils.get_jwt_secret()

