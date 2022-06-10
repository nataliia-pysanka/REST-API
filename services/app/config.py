from os import getenv

POSTGRES_USER = getenv('POSTGRES_USER')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')
POSTGRES_DB = getenv('POSTGRES_DB')
DB_PORT = getenv('DB_PORT')

ADMIN_ID = getenv('ADMIN_ID')


class Config:
    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:' \
                              f'{POSTGRES_PASSWORD}@localhost:5432' \
                              f'/{POSTGRES_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = getenv('SECRET_KEY')
