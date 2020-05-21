import os
from dotenv import load_dotenv

load_dotenv(verbose=True)


class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://USER:PASSWORD@HOST:PORT/NAME'
    SECRET_KEY = os.getenv('SECRET_KEY')
    TESTING = False


class Production(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('PRODUCTION_DATABASE_URI')


class Develop(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEVELOPMENT_DATABASE_URI')


class Testing(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('TESTING_DATABASE_URI')
    TESTING = False
