from flask import request
from flask_restx import Resource, fields, Namespace

from app.models.poster import PosterModel
from app.schemas.poster import PosterSchema

POSTER_NOT_FOUND = "Poster not found."
POSTER_ALREADY_EXISTS = "Poster '{}' already exists."

poster_ns = Namespace('poster', description='Item related operations')
posters_ns = Namespace('posters', description='Items related operations')

poster_schema = PosterSchema()
poster_list_schema = PosterSchema(many=True)


poster = posters_ns.model('Poster', {
    'url': fields.String('Path to the Poster')
})


class Poster(Resource):
    def get(self, _id):
        poster_data = PosterModel.find_by_id(_id)
        if poster_data:
            return poster_schema.dump(poster_data)
        return {'message': POSTER_NOT_FOUND}, 404

    def delete(self, _id):
        poster_data = PosterModel.find_by_id(_id)
        if poster_data:
            poster_data.delete_from_db()
            return {'message': "Poster deleted successfully"}, 200
        return {'message': POSTER_NOT_FOUND}, 404

    @poster_ns.expect(poster)
    def put(self, _id):
        poster_data = PosterModel.find_by_id(_id)
        poster_json = request.get_json()

        if poster_data:
            poster_data.name = poster_json['name']
            poster_data.description = poster_json['description']
            poster_data.enabled = poster_json['enabled']
        else:
            poster_data = poster_schema.load(poster_json)

        poster_data.save_to_db()
        return poster_schema.dump(poster_data), 200


class PosterList(Resource):
    @poster_ns.doc('Get all posters')
    def get(self):
        return poster_list_schema.dump(PosterModel.find_all()), 200

    @posters_ns.expect(poster)
    @posters_ns.doc('Create a poster')
    def post(self):
        poster_json = request.get_json()
        poster_data = poster_schema.load(poster_json)
        poster_data.save_to_db()

        return poster_schema.dump(poster_data), 201
