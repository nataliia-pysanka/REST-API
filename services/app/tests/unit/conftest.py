"""Configuration fixtures for unittests"""
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from mock_alchemy.mocking import AlchemyMagicMock

from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieDB
from app.crud.base import CRUDBase
from app.crud.movie import CRUDMovie
from app.domain.movie import DomainMovie

from app.models.director import Director
from app.schemas.director import DirectorCreate, DirectorDB
from app.crud.director import CRUDDirector
from app.domain.director import DomainDirector

from pydantic import ValidationError


# @pytest.fixture(name="type_error")
# def type_error():
#     """"""
#     return {"code": "invalidInput", "message": "Can't Create Object.",
#             "value": [{"loc": ["title"], "msg": "Use only letters.",
#                        "type": "value_error"}]}


@pytest.fixture(name='movie')
def mock_movie():
    """Movie sqlalchemy model mock set up."""
    my_model = Movie(
        title="Harry Potter",
        description="",
        date_release="2006-01-01",
        rating=6.9,
        id_user=1
    )
    return my_model


@pytest.fixture(name='movie_db')
def movie_db():
    """MovieDB pydantic model mock set up."""
    my_model = MovieDB(
        id=1,
        title="Harry Potter",
        description="",
        date_release="2006-01-01",
        rating=6.9,
        user={
            "date_birth": "2003-01-10",
            "date_registry": "2021-02-3",
            "id": "1",
            "name": "Victoria",
            "nickname": "Davisdiane_Admin",
            "role": {
                "description": "Could do anything",
                "enabled": "true",
                "id": "1",
                "name": "Admin"
            },
            "surname": "Duncan"
        }
    )
    return my_model


@pytest.fixture
def mock_get_sqlalchemy(mocker):
    """SQLAlchemy database mock set up."""
    mock = mocker.patch(
        "flask_sqlalchemy._QueryProperty.__get_all__").return_value \
        = mocker.Mock()
    return mock


@pytest.fixture
def flask_app_mock():
    """Flask application mock set up."""
    app_mock = Flask(__name__)
    app_mock.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app_mock)
    db.init_app(app_mock)

    return app_mock


@pytest.fixture(name="data")
def data():
    """Data for movie model"""
    return {"title": "Harry Potter", "date_release": "2022-06-14",
            "rating": "6.9"}


@pytest.fixture(name="data_director")
def data_director():
    """Data for director model"""
    return {"id": "1", "name": "Christofer", "surname": "Nolan",
            "date_birth": "1970-01-01"}


@pytest.fixture(name='movie_create')
def movie_create(mocker):
    """Flask application mock set up."""
    movie_create = mocker.patch.object(MovieCreate, 'parse_obj')
    movie_create.return_value = {"value": "OK"}
    return movie_create


@pytest.fixture(name='movie_create_fail')
def movie_create_fail(mocker):
    """MovieCreate pydantic model mock set up."""
    movie_create = mocker.patch.object(MovieCreate, '__init__')
    movie_create.raiseError.side_effect = ValidationError
    return movie_create


@pytest.fixture(name='movie_db')
def movie_db(mocker):
    """MovieDB pydantic model mock set up."""
    movie_db = mocker.patch.object(MovieDB, 'from_orm')
    movie_db.return_value = movie_db
    return movie_db


@pytest.fixture(name='crud_create')
def crud_create(mocker):
    """CRUDMovie class mock set up for function create."""
    crud = mocker.patch.object(CRUDMovie, 'create')
    crud.return_value = data
    return crud


@pytest.fixture(name='crud_read')
def crud_read(mocker):
    """CRUDMovie class mock set up for function read."""
    crud = mocker.patch.object(CRUDMovie, 'read')
    crud.return_value = data
    return crud


@pytest.fixture(name='crud_read_fail')
def crud_read_fail(mocker):
    """CRUDMovie class mock set up for function create None result."""
    crud = mocker.patch.object(CRUDMovie, 'read')
    crud.return_value = None
    return crud


@pytest.fixture(name='crud_read_all')
def crud_read_all(mocker):
    """CRUDMovie class mock set up for function read_all."""
    crud = mocker.patch.object(CRUDMovie, 'read_all')
    crud.return_value = []
    return crud


@pytest.fixture(name='crud_delete')
def crud_delete(mocker):
    """CRUDMovie class mock set up for function delete."""
    crud = mocker.patch.object(CRUDMovie, 'delete')
    crud.return_value = data
    return crud


@pytest.fixture(name='crud_delete_fail')
def crud_delete_fail(mocker):
    """CRUDMovie class mock set up for function delete None result."""
    crud = mocker.patch.object(CRUDMovie, 'delete')
    crud.return_value = None
    return crud


@pytest.fixture(name='crud_get_by_filter')
def crud_get_by_filter(mocker):
    """CRUDMovie class mock set up for function get_by_filter."""
    crud = mocker.patch.object(CRUDMovie, 'get_by_filter')
    crud.return_value = []
    return crud


@pytest.fixture(name='crud_get_by_filter_fail')
def crud_get_by_filter_fail(mocker):
    """CRUDMovie class mock set up for function get_by_filter None result."""
    crud = mocker.patch.object(CRUDMovie, 'get_by_filter')
    crud.return_value = None
    return crud


@pytest.fixture(name='session')
def session():
    """Session mock set up."""
    session = AlchemyMagicMock()
    return session


@pytest.fixture(name='domain_movie')
def domain_movie():
    """DomainMovie class mock set up."""
    domain = DomainMovie(CRUDMovie())
    return domain


@pytest.fixture(name='domain_director')
def domain_director():
    """DomainDirector class mock set up."""
    domain = DomainDirector(CRUDDirector())
    return domain


@pytest.fixture(name='director_db')
def director_db():
    """DirectorDB pydantic model mock set up."""
    my_model = DirectorDB(
        id=1,
        name="Christofer",
        surname="Nolan",
        date_birth="1970-01-01"
    )
    return my_model


@pytest.fixture(name='director_create')
def director_create(mocker):
    """DirectorDB pydantic model mock set up."""
    director_create = mocker.patch.object(DirectorCreate, 'parse_obj')
    director_create.return_value = data_director
    return director_create


@pytest.fixture(name='crud_director_create')
def crud_director_create(mocker):
    """CRUDMovie class mock set up for function create."""
    crud = mocker.patch.object(CRUDDirector, 'create')
    crud.return_value = data_director
    return crud


@pytest.fixture(name='crud_director_read')
def crud_director_read(mocker):
    """CRUDDirector class mock set up for function read."""
    crud = mocker.patch.object(CRUDDirector, 'read')
    crud.return_value = data_director
    return crud


@pytest.fixture(name='crud_director_read_fail')
def crud_director_read_fail(mocker):
    """CRUDDirector class mock set up for function create None result."""
    crud = mocker.patch.object(CRUDDirector, 'read')
    crud.return_value = None
    return crud


@pytest.fixture(name='crud_director_read_all')
def crud_director_read_all(mocker):
    """CRUDDirector class mock set up for function read_all."""
    crud = mocker.patch.object(CRUDDirector, 'read_all')
    crud.return_value = []
    return crud


@pytest.fixture(name='crud_director_delete')
def crud_director_delete(mocker):
    """CRUDDirector class mock set up for function delete."""
    crud = mocker.patch.object(CRUDDirector, 'delete')
    crud.return_value = data_director
    return crud


@pytest.fixture(name='crud_director_delete_fail')
def crud_director_delete_fail(mocker):
    """CRUDDirector class mock set up for function delete None result."""
    crud = mocker.patch.object(CRUDDirector, 'delete')
    crud.return_value = None
    return crud


@pytest.fixture(name='crud_director_get_by_filter')
def crud_director_get_by_filter(mocker):
    """CRUDDirector class mock set up for function get_by_filter."""
    crud = mocker.patch.object(CRUDDirector, 'get_by_filter')
    crud.return_value = []
    return crud


@pytest.fixture(name='crud_director_get_by_filter_fail')
def crud_director_get_by_filter_fail(mocker):
    """CRUDDirector class mock set up for function get_by_filter None result.
    """
    crud = mocker.patch.object(CRUDDirector, 'get_by_filter')
    crud.return_value = None
    return crud