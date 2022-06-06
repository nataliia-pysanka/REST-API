from flask import request
from flask_restx import Resource, fields, Namespace

from app.models.poster import PosterModel
from app.schemas.poster import PosterSchema
from app.CRUD.poster import CRUDPoster

from app.db import db

POSTER_NOT_FOUND = "Poster not found."
POSTER_ALREADY_EXISTS = "Poster '{}' already exists."

poster_ns = Namespace('poster', description='Item related operations')
posters_ns = Namespace('posters', description='Items related operations')

poster_schema = PosterSchema()
poster_list_schema = PosterSchema(many=True)

crud_poster = CRUDPoster(PosterModel)

poster = posters_ns.model('Poster', {
    'url': fields.String('Path to the Poster')
})


class Poster(Resource):
    def get(self, id: int):
        obj = crud_poster.read(db.session, id)
        if obj:
            return poster_schema.dump(obj), 200
        return {'message': POSTER_NOT_FOUND}, 404

    def delete(self, id: int):
        obj = crud_poster.delete(db.session, id)
        if obj:
            return {'message': "Poster deleted successfully"}, 200
        return {'message': POSTER_NOT_FOUND}, 404

    @poster_ns.expect(poster)
    def put(self, id: int):
        obj = crud_poster.update(db.session, request.get_json(), id)
        if obj:
            return {'message': "Poster updated successfully"}, 200
        return {'message': POSTER_NOT_FOUND}, 404


class PosterList(Resource):
    @poster_ns.doc('Get all the posters')
    def get(self):
        obj = crud_poster.read_all(db.session)
        if obj:
            return poster_list_schema.dump(obj), 200
        return {'message': POSTER_NOT_FOUND}, 404

    @posters_ns.expect(poster)
    @posters_ns.doc('Create a poster')
    def post(self):
        poster_json = request.get_json()
        poster_data = poster_schema.load(poster_json)
        obj = crud_poster.create(db.session, poster_data)
        if obj:

            return poster_schema.dump(poster_data), 201
