from flask import Blueprint, jsonify, redirect, url_for
from flask import request

from datetime import datetime


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
    genre = args.get('genre', '').split(' ')
    release_date = [datetime.strptime(item, '%Y-%m-%d')
               for item in args.get('release_date', '').split(',') if item]

    director = args.get('director', '').split(' ')

    offset = int(args.get('offset'), 0)
    limit = int(args.get('limit'), 10)

    id_genre = crud_genre.get_id_by_name(db.session, genre)
    id_director = crud_director.get_id_by_name(db.session, director)

    obj_all = crud_movie.get_by_filter(db.session,
                                   id_genre=id_genre,
                                   release_date=release_date,
                                   id_director=id_director,
                                   offset=offset,
                                   limit=limit)
    json = []
    for obj in obj_all:
        json.append(movie_schema.dump(obj))

    change_query = f'offset={offset}'
    query = request.full_path

    if json:
        next_url = query.replace(change_query, f'offset={offset + limit}')
    else:
        next_url = ''

    if offset >= limit:
        prev_url = query.replace(change_query, f'offset={offset - limit}')
    else:
        prev_url = ''

    return jsonify({'prev_url': prev_url, 'next_url': next_url,
                    'result': json})


