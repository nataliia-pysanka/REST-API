from flask import request
from flask_restx import Resource, fields, Namespace
from datetime import datetime

from app.models.director import DirectorModel
from app.schemas.director import DirectorSchema
from app.CRUD.director import CRUDDirector

from app.db import db

DIRECTOR_NOT_FOUND = "Director not found."
DIRECTOR_ALREADY_EXISTS = "Director '{}' already exists."

director_ns = Namespace('director', description='Item related operations')
directors_ns = Namespace('directors', description='Items related operations')

director_schema = DirectorSchema()
director_list_schema = DirectorSchema(many=True)
crud_director = CRUDDirector(DirectorModel)

director = directors_ns.model('Director', {
    'name': fields.String('Christopher'),
    'surname': fields.String('Nolan'),
    'date_birth': fields.Date(),
    'wiki_url': fields.String('https://en.wikipedia.org/wiki/Christopher_Nolan')
})


class Director(Resource):
    def get(self, id: int):
        obj = crud_director.read(db.session, id)
        if obj:
            return director_schema.dump(obj), 200
        return {'message': DIRECTOR_NOT_FOUND}, 404

    def delete(self, id: int):
        obj = crud_director.delete(db.session, id)
        if obj:
            return {'message': "Director deleted successfully"}, 200
        return {'message': DIRECTOR_NOT_FOUND}, 404

    @director_ns.expect(director)
    def put(self, id: int):
        obj = crud_director.update(db.session, request.get_json(), id)
        if obj:
            return {'message': "Director updated successfully"}, 200
        return {'message': DIRECTOR_NOT_FOUND}, 404


class DirectorList(Resource):
    @director_ns.doc('Get all the directors')
    def get(self):
        obj = crud_director.read_all(db.session)
        if obj:
            return director_list_schema.dump(obj), 200
        return {'message': DIRECTOR_NOT_FOUND}, 404

    @directors_ns.expect(director)
    @directors_ns.doc('Create a director')
    def post(self):
        director_json = request.get_json()
        director_data = director_schema.load(director_json)
        obj = crud_director.create(db.session, director_data)
        if obj:
            return director_schema.dump(director_data), 200
