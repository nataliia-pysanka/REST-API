from flask import Blueprint, jsonify, redirect, url_for
from flask import request

from app.models.movie import MovieModel
from app.models.genre import GenreModel
from app.models.director import DirectorModel
from app.schemas.movie import MovieSchema
from app.crud.movie import CRUDMovie
from app.crud.genre import CRUDGenre
from app.crud.director import CRUDDirector

from app.domain.movie import DomainMovie


movie_routes = Blueprint("movie_routes", __name__, url_prefix='/api')
movie_schema = MovieSchema()

movie_domain = DomainMovie(CRUDMovie())


@movie_routes.route('/search', methods=['GET'])
def search():
    args = request.args

    obj_all = movie_domain.get_movie_by_filter(args)
    json = [movie_schema.dump(obj) for obj in obj_all]

    offset = int(args.get('offset'), 0)
    limit = int(args.get('limit'), 10)

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


