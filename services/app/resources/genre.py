from flask import request
from flask_restx import Resource, fields, Namespace

from app.models.genre import GenreModel
from app.schemas.genre import GenreSchema
from app.CRUD.genre import CRUDGenre

from app.db import db

GENRE_NOT_FOUND = "Genre not found."
GENRE_ALREADY_EXISTS = "Genre '{}' already exists."

genre_ns = Namespace('genre', description='Item related operations')
genres_ns = Namespace('genres', description='Items related operations')

genre_schema = GenreSchema()
genre_list_schema = GenreSchema(many=True)

crud_genre = CRUDGenre(GenreModel)

genre = genres_ns.model('Genre', {
    'name': fields.String('Horror')
})


class Genre(Resource):
    def get(self, id: int):
        obj = crud_genre.read(db.session, id)
        if obj:
            return genre_schema.dump(obj), 200
        return {'message': GENRE_NOT_FOUND}, 404

    def delete(self, id: int):
        obj = crud_genre.delete(db.session, id)
        if obj:
            return {'message': "Genre deleted successfully"}, 200
        return {'message': GENRE_NOT_FOUND}, 404

    @genre_ns.expect(genre)
    def put(self, id: int):
        obj = crud_genre.update(db.session, request.get_json(), id)
        if obj:
            return {'message': "Genre updated successfully"}, 200
        return {'message': GENRE_NOT_FOUND}, 404


class GenreList(Resource):
    @genre_ns.doc('Get all the genres')
    def get(self):
        obj = crud_genre.read_all(db.session)
        if obj:
            return genre_list_schema.dump(obj), 200
        return {'message': GENRE_NOT_FOUND}, 404

    @genres_ns.expect(genre)
    @genres_ns.doc('Create a genre')
    def post(self):
        genre_json = request.get_json()
        genre_data = genre_schema.load(genre_json)
        obj = crud_genre.create(db.session, genre_data)
        if obj:
            return genre_schema.dump(genre_data), 200
