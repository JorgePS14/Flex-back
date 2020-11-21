class Config(object):
    SECRET_KEY = 'FLEXPROJECT'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:admin12345@flexproyect.cqwbrqenmt7b.us-east-2.rds.amazonaws.com/flexProyect"
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True

class Defaults(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 499
    SQLALCHEMY_POOL_TIMEOUT = 20

class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True