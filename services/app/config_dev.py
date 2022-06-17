from os import getenv

POSTGRES_USER = getenv('POSTGRES_USER')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')
POSTGRES_DB = getenv('POSTGRES_DB')
DB_PORT = getenv('DB_PORT')
DB_HOST = getenv('DB_HOST')
ADMIN_ID = getenv('ADMIN_ID')


class Config:
    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:' \
                              f'{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}' \
                              f'/{POSTGRES_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = getenv('SECRET_KEY')

    ADMIN_NUM = getenv('ADMIN_NUM')
    USER_NUM = getenv('USER_NUM')
    DIRECTOR_NUM = getenv('DIRECTOR_NUM')
    POSTER_NUM = getenv('POSTER_NUM')
    MOVIE_NUM = getenv('MOVIE_NUM')

    ADMIN_ID = ADMIN_ID
