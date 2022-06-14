import pytest
from pydantic import ValidationError
from app.schemas.movie import MovieCreate


@pytest.fixture(name="data_director")
def data_director():
    """Data for director model"""
    return {"name": "", "surname": "Nolan", "date_birth": "1970-01-01"}


@pytest.fixture(name="data_movie")
def data():
    """Data for movie model"""
    return {"title": "1234456", "date_release": "2022-06-14"}


def test_movie_create_model_with_invalid_data(flask_app_mock, data_movie):
    """Calls method for MovieCreate"""
    with pytest.raises(ValidationError):
        MovieCreate.parse_obj(data_movie)


