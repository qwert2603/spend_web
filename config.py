import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

    @staticmethod
    def records_user_id():
        from manage import app
        return app.config['RECORDS_USER_ID']


class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = '1918'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db_dev.sqlite')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@127.0.0.1:5432/spend_test'
    RECORDS_USER_ID = 2


class ProdConfig(Config):
    DEBUG = True
    SECRET_KEY = '1918'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@127.0.0.1:5432/spend'
    RECORDS_USER_ID = 5


config = {
    'dev': DevConfig,
    'prod': ProdConfig,
}
