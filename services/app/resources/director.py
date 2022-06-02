from flask import request
from flask_restx import Resource, fields, Namespace
from datetime import datetime

from app.models.director import DirectorModel
from app.schemas.director import DirectorSchema

DIRECTOR_NOT_FOUND = "Director not found."
DIRECTOR_ALREADY_EXISTS = "Director '{}' already exists."

director_ns = Namespace('director', description='Item related operations')
directors_ns = Namespace('directors', description='Items related operations')

director_schema = DirectorSchema()
director_list_schema = DirectorSchema(many=True)


director = directors_ns.model('Director', {
    'name': fields.String('Christopher'),
    'surname': fields.String('Nolan'),
    'date_birth': fields.Date(),
    'wiki_url': fields.String('https://en.wikipedia.org/wiki/Christopher_Nolan')
})


class Director(Resource):
    def get(self, _id):
        director_data = DirectorModel.find_by_id(_id)
        if director_data:
            return director_schema.dump(director_data)
        return {'message': DIRECTOR_NOT_FOUND}, 404

    def delete(self, _id):
        director_data = DirectorModel.find_by_id(_id)
        if director_data:
            director_data.delete_from_db()
            return {'message': "Item deleted successfully"}, 200
        return {'message': DIRECTOR_NOT_FOUND}, 404

    @director_ns.expect(director)
    def put(self, _id):
        director_data = DirectorModel.find_by_id(_id)
        director_json = request.get_json()

        if director_data:
            director_data.title = director_json['title']
            director_data.description = director_json['description']
            director_data.date_release = director_json['date_release']
            director_data.rating = director_json['rating']
            director_data.id_director = director_json['id_director']
            director_data.id_poster = director_json['id_poster']
            director_data.id_user = director_json['id_user']
        else:
            director_data = director_schema.load(director_json)

        director_data.save_to_db()
        return director_schema.dump(director_data), 200


class DirectorList(Resource):
    @director_ns.doc('Get all the directors')
    def get(self):
        return director_list_schema.dump(DirectorModel.find_all()), 200

    @directors_ns.expect(director)
    @directors_ns.doc('Create a director')
    def post(self):
        director_json = request.get_json()
        print(f'director_json - {director_json}')
        director_data = director_schema.load(director_json)
        print(f'director_data - {director_data}')
        director_data.save_to_db()

        return director_schema.dump(director_data), 201
