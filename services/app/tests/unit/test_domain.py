"""Tests for domain part of project"""
from pydantic import ValidationError


# domain movie
def test_movie_create_with_valid_data(flask_app_mock, data, movie,
                                      domain_movie, movie_db, movie_create,
                                      session, crud_create):
    """Callss method for creating movie with valid data and check result"""
    with flask_app_mock.app_context():
        result, err = domain_movie.create(session, data)

    assert result == movie_db.dict()
    assert err is None


def test_movie_create_with_invalid_data(flask_app_mock, data, movie,
                                        domain_movie, movie_db, session,
                                        movie_create_fail, crud_create):
    """Calls method for crating movie with invalid data and check result"""
    with flask_app_mock.app_context():
        result, err = domain_movie.create(session, 1)

    assert result is None
    assert isinstance(err, ValidationError)


def test_movie_read_valid_id(flask_app_mock, domain_movie, session, crud_read,
                             movie_db, data):
    """Calls method for reading movie with valid id and check result"""
    with flask_app_mock.app_context():
        result = domain_movie.read(session, 1)

    assert result == movie_db.dict()


def test_movie_read_invalid_id(flask_app_mock, domain_movie, session,
                               crud_read_fail,
                               movie_db, data):
    """Calls method for reading movie with invalid id and check result"""
    with flask_app_mock.app_context():
        result = domain_movie.read(session, 1)

    assert result is None


def test_movie_read_all(flask_app_mock, domain_movie, session, crud_read_all,
                        movie_db, data):
    """Calls method for reading all movies"""
    with flask_app_mock.app_context():
        result = domain_movie.read_all(session)

    assert result == []


def test_movie_delete_with_valid_id(flask_app_mock, domain_movie, session,
                                    crud_delete, data):
    """Calls method for deleting movie with valid id"""
    with flask_app_mock.app_context():
        result = domain_movie.delete(session, 1)

    assert result is True


def test_movie_delete_with_invalid_id(flask_app_mock, domain_movie, session,
                                      crud_delete_fail, data):
    """Calls method for deleting movie with invalid id"""
    with flask_app_mock.app_context():
        result = domain_movie.delete(session, 1)

    assert result is None


def test_movie_get_by_filter_with_no_args(flask_app_mock, domain_movie,
                                          session,
                                          movie_db, crud_read_all):
    """Calls method for filtering movie with None data filters"""
    with flask_app_mock.app_context():
        result = domain_movie.get_movie_by_filter(session,
                                                  {'genre': None,
                                                   'release_date': None,
                                                   'director': None})

    assert result == []


def test_movie_get_by_filter_with_part_args(flask_app_mock, domain_movie,
                                            session,
                                            movie_db, crud_get_by_filter_fail):
    """Calls method for filtering movie with part data filters"""
    with flask_app_mock.app_context():
        result = domain_movie.get_movie_by_filter(session,
                                                  {'genre': 'horror',
                                                   'release_date': "",
                                                   'director': ""})

    assert result is None


def test_movie_get_by_filter_with_args(flask_app_mock, domain_movie, session,
                                       movie_db, crud_get_by_filter):
    """Calls method for filtering movie with full data filters"""
    with flask_app_mock.app_context():
        result = domain_movie.get_movie_by_filter(session,
                                     {'genre': 'horror',
                                      'release_date': "2000-02-02,2020-02-02",
                                      'director': "nolan"})

    assert result is None


# domain Director
# def test_director_create_with_valid_data(flask_app_mock, data_director, movie,
#                                          domain_director, director_db,
#                                          director_create, session, crud_create):
#     """Calls method for create director with valid data"""
#     with flask_app_mock.app_context():
#         result, err = domain_director.create(session, data_director)
#
#     assert result == director_db.dict()
#     assert err is None


# def test_director_create_with_invalid_data(flask_app_mock, data, movie,
#                                            domain_director, director_db, session,
#                                            director_create_fail, crud_create,
#                                            type_error):
#     with flask_app_mock.app_context():
#         result, err = domain_director.create(session, 1)
#
#     assert result is None
#     assert isinstance(err, ValidationError)
# #
#
# def test_director_read_valid_id(flask_app_mock, domain_director, session,
#                                 crud_read,
#                                 director_db, data):
#     with flask_app_mock.app_context():
#         result = domain_director.read(session, 1)
#
#     assert result == director_db.dict()
#
#
# def test_director_read_invalid_id(flask_app_mock, domain_director, session,
#                                   crud_read_fail,
#                                   director_db, data):
#     with flask_app_mock.app_context():
#         result = domain_director.read(session, 1)
#
#     assert result is None
#
#
# def test_director_read_all(flask_app_mock, domain_director, session,
#                            crud_read_all,
#                            director_db, data):
#     with flask_app_mock.app_context():
#         result = domain_director.read_all(session)
#
#     assert result == []
#
#
# def test_director_delete_with_valid_id(flask_app_mock, domain_director,
#                                        session,
#                                        crud_delete, data):
#     with flask_app_mock.app_context():
#         result = domain_director.delete(session, 1)
#
#     assert result is True
#
#
# def test_director_delete_with_invalid_id(flask_app_mock, domain_director,
#                                          session,
#                                          crud_delete_fail, data):
#     with flask_app_mock.app_context():
#         result = domain_director.delete(session, 1)
#
#     assert result is None
#
#
# def test_director_get_id_by_name(flask_app_mock, domain_director,
#                                  session,
#                                  director_db, crud_get_by_filter):
#     with flask_app_mock.app_context():
#         result = domain_director.get_movie_by_filter(session,
#                                                      {'genre': 'horror',
#                                                       'release_date': "2000-02-02,2020-02-02",
#                                                       'director': "nolan"})
#
#     assert result is None
#
#     def get_id_by_name(self, session: Session, name_list: List[str]) -> List[
#         Any]:
#         if name_list:
#             return self.crud.get_id_by_name(session, name_list)
#         return []
