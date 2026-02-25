import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# load_env
load_dotenv(override=True)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default')
    PORT = int(os.getenv('PORT'))

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO')
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI')


class TestConfig(Config):
    pass


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URI')
    DEBUG = False


config_dict = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,

    'default': DevConfig,
}