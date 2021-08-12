import os

class Config(object):
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST') or 'localhost:5432'
    POSTGRES_DB = os.environ.get('POSTGRES_DB') or 'integration'
    POSTGRES_USER = os.environ.get('POSTGRES_USER') or 'user'
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD') or 'pass'
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1cabca0cd34552295328a40ad75954049ec344d556390ac4'