from flask import request
from flask_restx import Resource, fields, Namespace

import app.util.responses as resp
from app.util.responses import response_with
from app.crud.genre import CRUDGenre
from app.domain.genre import DomainGenre

from app.db import db

genre_ns = Namespace('genre', description='Item related operations')
genres_ns = Namespace('genres', description='Items related operations')

genre_domain = DomainGenre(CRUDGenre())

genre = genres_ns.model('Genre', {
    'name': fields.String('Horror')
})


class Genre(Resource):
    def get(self, id: int):
        obj = genre_domain.read(db.session, id)
        if obj:
            return response_with(resp.SUCCESS_200, value=obj)
        return response_with(resp.NOT_FOUND_404,
                             message=resp.NOT_FOUND)

    def delete(self, id: int):
        obj = genre_domain.delete(db.session, id)
        if obj:
            return response_with(resp.SUCCESS_200,
                                 message=resp.WAS_DELETED,
                                 value=obj)
        return response_with(resp.NOT_FOUND_404,
                             message=resp.NOT_FOUND)

    @genre_ns.expect(genre)
    def put(self, id: int):
        data = request.get_json()
        obj, err = genre_domain.update(db.session, data, id)
        if err:
            return response_with(resp.INVALID_INPUT_422,
                                 message=resp.CANT_UPDATE,
                                 value=err.errors())
        if obj:
            return response_with(resp.SUCCESS_201,
                                 message=resp.UPDATED,
                                 value=obj)

        return response_with(resp.NOT_FOUND_404,
                             message=resp.NOT_FOUND)


class GenreList(Resource):
    @genres_ns.doc('Get all the genres')
    def get(self):
        obj = genre_domain.read_all(db.session)
        if obj:
            return response_with(resp.SUCCESS_200, value=obj)
        return response_with(resp.NOT_FOUND_404,
                             message=resp.NOT_FOUND)

    @genres_ns.expect(genre)
    @genres_ns.doc('Create a genre')
    def post(self):
        data = request.get_json()
        obj, err = genre_domain.create(db.session, data)
        if err:
            return response_with(resp.INVALID_INPUT_422,
                                 message=resp.CANT_CREATE,
                                 value=err.errors())
        if obj:
            return response_with(resp.SUCCESS_201, value=obj)

        return response_with(resp.INVALID_INPUT_422,
                             message=resp.CANT_CREATE)
