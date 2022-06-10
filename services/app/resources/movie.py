from flask import request
from flask_restx import Resource, fields, Namespace
from flask_login import login_required, current_user

from app.schemas.movie import MovieSchema
from app.crud.movie import CRUDMovie
from app.domain.movie import DomainMovie


MOVIE_NOT_FOUND = "Movie not found."
MOVIE_ALREADY_EXISTS = "Movie '{}' already exists."

movie_ns = Namespace('movie', description='Item related operations')
movies_ns = Namespace('movies', description='Items related operations')
search_ns = Namespace('movies', description='Items related operations')

movie_schema = MovieSchema()
movie_list_schema = MovieSchema(many=True)

movie_domain = DomainMovie(CRUDMovie())

movie = movies_ns.model('Movie', {
    'title': fields.String('Name of the Movie'),
    'description': fields.String('Description of the Movie'),
    'date_release': fields.Date(),
    'rating': fields.Float(0.00),
    'id_genre': fields.Integer,
    'id_director': fields.Integer,
    'id_poster': fields.Integer,
    'id_user': fields.Integer
})


class Movie(Resource):
    def get(self, id):
        obj = movie_domain.read(id)
        if obj:
            return movie_schema.dump(obj), 200
        return {'message': MOVIE_NOT_FOUND}, 404

    @login_required
    def delete(self, id):
        user_id = movie_domain.read(id).id_user
        if current_user.id == user_id or current_user.is_admin():
            obj = movie_domain.delete(id)
            if obj:
                return {'message': "Movie deleted successfully"}, 200
            return {'message': MOVIE_NOT_FOUND}, 404
        else:
            return {'message': "No rights for deleting"}, 404

    @movie_ns.expect(movie)
    @login_required
    def put(self, id):
        obj = movie_domain.update(request.get_json(), id)
        if obj:
            return {'message': "Movie updated successfully"}, 200
        return {'message': MOVIE_NOT_FOUND}, 404


class MovieList(Resource):
    @movies_ns.doc('Get all the movies')
    def get(self):
        obj = movie_domain.read_all()
        if obj:
            return movie_list_schema.dump(obj), 200
        return {'message': MOVIE_NOT_FOUND}, 404

    @movies_ns.expect(movie)
    @movies_ns.doc('Create a movie')
    @login_required
    def post(self):
        movie_json = request.get_json()
        movie_data = movie_schema.load(movie_json)
        obj = movie_domain.create(movie_data)
        if obj:
            return movie_schema.dump(movie_data), 201


# class MovieSearch(Resource):
# @search_ns.doc('Get all the movies')
#     def get(self):
#         args = request.args
#
#         obj_all = movie_domain.get_movie_by_filter(args)
#         json = [movie_schema.dump(obj) for obj in obj_all]
#
#         offset = int(args.get('offset'), 0)
#         limit = int(args.get('limit'), 10)
#
#         change_query = f'offset={offset}'
#         query = request.full_path
#
#         if json:
#             next_url = query.replace(change_query, f'offset={offset + limit}')
#         else:
#             next_url = ''
#
#         if offset >= limit:
#             prev_url = query.replace(change_query, f'offset={offset - limit}')
#         else:
#             prev_url = ''
#
#         return jsonify({'prev_url': prev_url, 'next_url': next_url,
#                         'result': json})