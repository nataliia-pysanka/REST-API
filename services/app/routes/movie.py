from flask import Blueprint
from flask import request


from app.models.movie import MovieModel
from app.models.genre import GenreModel
from app.models.director import DirectorModel
from app.schemas.movie import MovieSchema
from app.CRUD.movie import CRUDMovie
from app.CRUD.genre import CRUDGenre
from app.CRUD.director import CRUDDirector

from app.db import db

movie_routes = Blueprint("movie_routes", __name__, url_prefix='/api')
movie_schema = MovieSchema()

crud_movie = CRUDMovie(MovieModel)
crud_genre = CRUDGenre(GenreModel)
crud_director = CRUDDirector(DirectorModel)


@movie_routes.route('/search', methods=['GET'])
def search():
    args = request.args
    genre = args.get('genre')
    release = args.get('release')
    director = args.get('director')

    id_genre = crud_genre.get_id_by_name(db.session, genre)
    id_director = crud_director.get_id_by_name(db.session, director)
    print(id_genre, id_director)
    obj = crud_movie.get_by_filter(db.session,
                                   id_genre=id_genre,
                                   release=release,
                                   id_director=id_director)

    return movie_schema.dump(obj), 200
