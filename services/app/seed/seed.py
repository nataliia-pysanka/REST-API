import random
import datetime
from faker import Faker
from sqlalchemy.orm import Session

from app.models.director import DirectorModel
from app.models.genre import GenreModel
from app.models.role import RoleModel
from app.models.poster import PosterModel
from app.models.user import UserModel
from app.models.movie import MovieModel

from app.CRUD.base import CRUDBase
from app.CRUD.director import CRUDDirector

from typing import TypeVar, Any

fake = Faker()

BaseModel = TypeVar("BaseModel")


def is_exist(session: Session, model: BaseModel, attr: Any):
    obj = CRUDBase(model).get_id_by_name(session, attr)
    if obj:
        return True
    return False


def seed_users_by_roles(session: Session, num: int, role: int):
    counter = 1
    while counter < num + 1:
        nickname = fake.simple_profile()['username'] + str(counter)
        user_json = {'nickname': nickname,
                     'password': fake.password(),
                     'name': fake.first_name(),
                     'surname': fake.last_name(),
                     'date_birth': (fake.date_between(start_date='-70y',
                                                      end_date='-15y')),
                     'date_registry': (fake.date_between(start_date='-2y')),
                     'id_role': str(role)
                     }
        CRUDBase(UserModel).create(session, user_json)
        counter += 1


def seed_directors(session: Session, num: int):
    counter = 0
    while counter < num:
        name = fake.first_name()
        surname = fake.last_name()
        if is_exist(session, DirectorModel, name) and \
                is_exist(session, DirectorModel, surname):
            continue
        director_json = {'name': name,
                         'surname': surname,
                         'date_birth': str(fake.date_between(start_date='-80y',
                                                             end_date='-22y')),
                         'wiki_url': f'https://en.wikipedia.org/wiki/'
                                     f'{name}_{surname}'
                         }
        CRUDBase(DirectorModel).create(session, director_json)
        counter += 1


GENRES = ['Action', 'Comedy', 'Drama', 'Fantasy', 'Horror', 'Mystery',
          'Romance', 'Thriller', 'Western', 'Crime', 'Thriller', 'Disaster',
          'Thriller', 'Psychological', 'Thriller', 'Techno', 'Thriller']


def seed_genres(session: Session):
    genre_json = {"name": None}
    for genre in GENRES:
        genre_json['name'] = genre
        CRUDBase(GenreModel).create(session, genre_json)


def seed_roles(session: Session):
    data_json = [
        {
            "name": "Admin",
            "description": "Could do anything",
            "enabled": True
        },
        {
            "name": "User",
            "description": "Could do something",
            "enabled": True
        }
    ]
    for data in data_json:
        CRUDBase(RoleModel).create(session, data)


def seed_posters(session: Session, num: int):
    counter = 1
    while counter < num + 1:
        data_json = {'url': f'https://poster/{counter}'}
        CRUDBase(PosterModel).create(session, data_json)
        counter += 1


def seed_movies(session: Session, num: int):
    counter = 0
    while counter < num:
        id_director = random.choice([None, fake.random_int(min=1, max=2000)])
        birth = CRUDDirector(DirectorModel).get_birth_by_id(session,
                                                            id_director)
        if birth:
            year_delta = datetime.datetime.now().year - birth.year - 21
        else:
            year_delta = 70
        movie_json = {
            'title': fake.text(max_nb_chars=20),
            'description': fake.text(max_nb_chars=160),
            'date_release': str(fake.date_between(start_date=f'-{year_delta}y')),
            'rating': fake.random_digit() + (fake.random_digit() * 0.1),
            'id_director': id_director,
            'id_poster': random.choice([None, fake.random_int(min=1,
                                                              max=20000)]),
            'id_user': fake.random_int(min=1, max=2000)
        }

        CRUDBase(MovieModel).create(session, movie_json)
        counter += 1
