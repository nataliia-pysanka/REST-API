from flask import request
from flask_restx import Resource, fields, Namespace
from flask_filter.query_filter import query_with_filters

from app.models.movie import MovieModel
from app.schemas.movie import MovieSchema
from app.CRUD.movie import CRUDMovie

from app.db import db

MOVIE_NOT_FOUND = "Movie not found."
MOVIE_ALREADY_EXISTS = "Movie '{}' already exists."

movie_ns = Namespace('movie', description='Item related operations')
movies_ns = Namespace('movies', description='Items related operations')
search_ns = Namespace('movies', description='Items related operations')

movie_schema = MovieSchema()
movie_list_schema = MovieSchema(many=True)

crud_movie = CRUDMovie(MovieModel)

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
        obj = crud_movie.read(db.session, id)
        if obj:
            return movie_schema.dump(obj), 200
        return {'message': MOVIE_NOT_FOUND}, 404

    def delete(self, id):
        obj = crud_movie.delete(db.session, id)
        if obj:
            return {'message': "Movie deleted successfully"}, 200
        return {'message': MOVIE_NOT_FOUND}, 404

    @movie_ns.expect(movie)
    def put(self, id):
        obj = crud_movie.update(db.session, request.get_json(), id)
        if obj:
            return {'message': "Movie updated successfully"}, 200
        return {'message': MOVIE_NOT_FOUND}, 404


class MovieList(Resource):
    @movie_ns.doc('Get all the movies')
    def get(self):
        obj = crud_movie.read_all(db.session)
        if obj:
            return movie_list_schema.dump(obj), 200
        return {'message': MOVIE_NOT_FOUND}, 404

    @movies_ns.expect(movie)
    @movies_ns.doc('Create a movie')
    def post(self):
        movie_json = request.get_json()
        movie_data = movie_schema.load(movie_json)
        obj = crud_movie.create(db.session, movie_data)
        if obj:
            return movie_schema.dump(movie_data), 201


class MovieSearch(Resource):
    @search_ns.doc('Get movies by filters')
    def get(self):
        print('hello')
        query = request.args.get("query")
        print(f'query {query}')
        return f"Query expression was: {query}"
