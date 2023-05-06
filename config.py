import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    SECRET = "secret-key"
    SECRET_KEY = "some secrete"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class MySQLConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql@localhost:3306/chembreakage'


class Production(Config):
    DEBUG = False
    TESTING = False


class Testing(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    TESTING = True
