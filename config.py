import os
class Config:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY') or 'bOOk-a-Meal'

    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    """ ADD DEVELOPMENT CONFIGURATIONS """
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY') or 'bOOk-a-Meal'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEVELOP_DATABASE_URL',
        'postgresql://localhost/book_a_meal_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class TestingConfig(Config):
    """ ADD CONFIGURATIONS TO USE WHILE TESTING """
    TESTING = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TESTING_DATABASE_URL',
        'postgresql://localhost/book_a_meal_test_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

config = {
    'testing': TestingConfig,
    'development': DevConfig,
    'default': Config
}
