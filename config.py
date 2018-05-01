import os
class Config:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')

class TestingConfig(Config):
    TESTING = True

config = {
    'testing': TestingConfig,
    'default': Config
}