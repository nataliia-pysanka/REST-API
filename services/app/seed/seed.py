"""Module for seeding database"""
import random
import datetime
from faker import Faker
from sqlalchemy.orm import Session

from app.domain.director import DomainDirector
from app.domain.genre import DomainGenre
from app.domain.role import DomainRole
from app.domain.poster import DomainPoster
from app.domain.user import DomainUser
from app.domain.movie import DomainMovie

from app.crud.director import CRUDDirector
from app.crud.genre import CRUDGenre
from app.crud.role import CRUDRole
from app.crud.poster import CRUDPoster
from app.crud.user import CRUDUser
from app.crud.movie import CRUDMovie
from app.crud.base import CRUDBase

from typing import TypeVar, Any

from app.schemas.director import DirectorCreate

fake = Faker()

BaseCreate = TypeVar("BaseCreate")


def is_exist(session: Session, attr: Any) -> bool:
    """Check if field already exist in DB"""
    obj = CRUDDirector().get_id_by_name(session, attr)
    if obj:
        return True
    return False


def seed_users_by_roles(session: Session, num: int, role: int):
    """Seed users by roles"""
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
        DomainUser(CRUDUser()).create(session, user_json)
        counter += 1


def seed_directors(session: Session, num: int):
    """Seed directors"""
    counter = 0
    while counter < num:
        name = fake.first_name()
        surname = fake.last_name()
        if is_exist(session, name) and \
                is_exist(session, surname):
            continue
        director_json = {'name': name,
                         'surname': surname,
                         'date_birth': str(fake.date_between(start_date='-80y',
                                                             end_date='-22y')),
                         'wiki_url': f'https://en.wikipedia.org/wiki/'
                                     f'{name}_{surname}'
                         }
        DomainDirector(CRUDDirector()).create(session, director_json)
        counter += 1


GENRES = ['Action', 'Comedy', 'Drama', 'Fantasy', 'Horror', 'Mystery',
          'Romance', 'Thriller', 'Western', 'Crime', 'Thriller', 'Disaster',
          'Thriller', 'Psychological', 'Thriller', 'Techno', 'Thriller']


def seed_genres(session: Session):
    """Seed genres"""
    genre_json = {"name": None}
    for genre in GENRES:
        genre_json['name'] = genre
        DomainGenre(CRUDGenre()).create(session, genre_json)


def seed_roles(session: Session):
    """Seed roles"""
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
        DomainRole(CRUDRole()).create(session, data)


def seed_posters(session: Session, num: int):
    """Seed posters"""
    counter = 1
    while counter < num + 1:
        data_json = {'url': f'https://poster/{counter}'}
        DomainPoster(CRUDPoster()).create(session, data_json)
        counter += 1


def seed_movies(session: Session, num: int):
    """Seed movies"""
    counter = 0
    while counter < num:
        id_director = random.choice([None, fake.random_int(min=1, max=num)])

        birth = CRUDDirector().get_birth_by_id(session, id_director)
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
                                                              max=num)]),
            'id_user': fake.random_int(min=1, max=310),
            'id_genre': fake.random_int(min=1, max=len(GENRES))
        }

        DomainMovie(CRUDMovie()).create(session, movie_json)
        counter += 1
