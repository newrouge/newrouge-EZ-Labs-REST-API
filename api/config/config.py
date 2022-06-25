import os
from decouple import AutoConfig,config
from datetime import timedelta

BASE_DIR=os.path.dirname(os.path.realpath(__file__))



class Config:
    SECRET_KEY= config('SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES= timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(minutes=60)
    JWT_SECRET_KEY=config("JWT_SECRET_KEY")


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(BASE_DIR,'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=True
    DEBUG=True

config_dict={
    'dev':DevConfig,
}