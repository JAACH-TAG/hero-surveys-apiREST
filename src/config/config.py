# src/config/config.py
from datetime import timedelta
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class BaseConfig:
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_TOKEN_LOCATION = ['cookies'],
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds = 120),
    JWT_COOKIE_CSRF_PROTECT = True,
    JWT_CSRF_CHECK_FORM = True,

# class DevelopmentConfig(BaseConfig):
#     DEBUG = True
#     BCRYPT_LOG_ROUNDS = 4
#     SECRET_KEY = environ.get("SECRET_KEY"),
#     SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI_TEST"),
#     JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")

class ProductionConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = environ.get("SECRET_KEY")
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")
    DATABASE_URL = environ.get("DATABASE_URL")
    
