from flask import request
from flask_restx import Resource, fields, Namespace

from app.models.genre import GenreModel
from app.schemas.genre import GenreSchema

GENRE_NOT_FOUND = "Genre not found."
GENRE_ALREADY_EXISTS = "Genre '{}' already exists."

genre_ns = Namespace('genre', description='Item related operations')
genres_ns = Namespace('genres', description='Items related operations')

genre_schema = GenreSchema()
genre_list_schema = GenreSchema(many=True)


genre = genres_ns.model('Genre', {
    'name': fields.String('Horror')
})


class Genre(Resource):
    def get(self, _id):
        genre_data = GenreModel.find_by_id(_id)
        if genre_data:
            return genre_schema.dump(genre_data)
        return {'message': GENRE_NOT_FOUND}, 404

    def delete(self, _id):
        genre_data = GenreModel.find_by_id(_id)
        if genre_data:
            genre_data.delete_from_db()
            return {'message': "Genre deleted successfully"}, 200
        return {'message': GENRE_NOT_FOUND}, 404

    @genre_ns.expect(genre)
    def put(self, _id):
        genre_data = GenreModel.find_by_id(_id)
        genre_json = request.get_json()

        if genre_data:
            genre_data.name = genre_json['name']
            genre_data.description = genre_json['description']
            genre_data.enabled = genre_json['enabled']
        else:
            genre_data = genre_schema.load(genre_json)

        genre_data.save_to_db()
        return genre_schema.dump(genre_data), 200


class GenreList(Resource):
    @genre_ns.doc('Get all genres')
    def get(self):
        return genre_list_schema.dump(GenreModel.find_all()), 200

    @genres_ns.expect(genre)
    @genres_ns.doc('Create a genre')
    def post(self):
        genre_json = request.get_json()
        genre_data = genre_schema.load(genre_json)
        genre_data.save_to_db()

        return genre_schema.dump(genre_data), 201
