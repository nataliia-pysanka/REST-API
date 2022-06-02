from flask import request
from flask_restx import Resource, fields, Namespace

from app.models.movie import MovieModel
from app.schemas.movie import MovieSchema

MOVIE_NOT_FOUND = "Movie not found."
MOVIE_ALREADY_EXISTS = "Movie '{}' already exists."

movie_ns = Namespace('movie', description='Item related operations')
movies_ns = Namespace('movies', description='Items related operations')

movie_schema = MovieSchema()
movie_list_schema = MovieSchema(many=True)


movie = movies_ns.model('Movie', {
    'title': fields.String('Name of the Movie'),
    'description': fields.String('Description of the Movie'),
    'date_release': fields.Date(),
    'rating': fields.Float(0.00),
    'id_director': fields.Integer,
    'id_poster': fields.Integer,
    'id_user': fields.Integer
})


class Movie(Resource):
    def get(self, _id):
        movie_data = MovieModel.find_by_id(_id)
        if movie_data:
            return movie_schema.dump(movie_data)
        return {'message': MOVIE_NOT_FOUND}, 404

    def delete(self, _id):
        movie_data = MovieModel.find_by_id(_id)
        if movie_data:
            movie_data.delete_from_db()
            return {'message': "Item deleted successfully"}, 200
        return {'message': MOVIE_NOT_FOUND}, 404

    @movie_ns.expect(movie)
    def put(self, _id):
        movie_data = MovieModel.find_by_id(_id)
        movie_json = request.get_json()

        if movie_data:
            movie_data.title = movie_json['title']
            movie_data.description = movie_json['description']
            movie_data.date_release = movie_json['date_release']
            movie_data.rating = movie_json['rating']
            movie_data.id_director = movie_json['id_director']
            movie_data.id_poster = movie_json['id_poster']
            movie_data.id_user = movie_json['id_user']
        else:
            movie_data = movie_schema.load(movie_json)

        movie_data.save_to_db()
        return movie_schema.dump(movie_data), 200


class MovieList(Resource):
    @movie_ns.doc('Get all the movies')
    def get(self):
        return movie_list_schema.dump(MovieModel.find_all()), 200

    @movies_ns.expect(movie)
    @movies_ns.doc('Create a movie')
    def post(self):
        movie_json = request.get_json()
        print(f'movie_json - {movie_json}')
        movie_data = movie_schema.load(movie_json)
        print(f'movie_data - {movie_data}')
        movie_data.save_to_db()

        return movie_schema.dump(movie_data), 201
