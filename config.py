import os
class Config:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')

class DevConfig(Config):
    """ ADD DEVELOPMENT CONFIGURATIONS """
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEVELOP_DATABASE_URL',
        'postgresql://localhost/book_a_meal_db')


class TestingConfig(Config):
    """ ADD CONFIGURATIONS TO USE WHILE TESTING """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TESTING_DATABASE_URL',
        'postgresql://localhost/book_a_meal_test_db')

config = {
    'testing': TestingConfig,
    'default': Config
}