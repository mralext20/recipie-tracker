from os import environ


class Config:
    SQLALCHEMY_DATABASE_URI = environ.get('POSTGRES_URI') or 'sqlite:///../db.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = environ.get('SECRET_KEY') or 'lol secret keys'
