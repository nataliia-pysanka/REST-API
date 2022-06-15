from flask import request
from flask_restx import Resource, fields, Namespace

import app.util.responses as resp
from app.util.responses import response_with
from app.domain.poster import DomainPoster
from app.crud.poster import CRUDPoster

from app.db import db

poster_ns = Namespace('poster', description='Item related operations')
posters_ns = Namespace('posters', description='Items related operations')

poster_domain = DomainPoster(CRUDPoster())

poster = posters_ns.model('Poster', {
    'url': fields.String('Path to the Poster')
})


class Poster(Resource):
    def get(self, id: int):
        obj = poster_domain.read(db.session, id)
        if obj:
            return response_with(resp.SUCCESS_200, value=obj)
        return response_with(resp.NOT_FOUND_404,
                             message=resp.NOT_FOUND)

    def delete(self, id: int):
        obj = poster_domain.delete(db.session, id)
        if obj:
            return response_with(resp.SUCCESS_200,
                                 message=resp.WAS_DELETED,
                                 value=obj)
        return response_with(resp.NOT_FOUND_404,
                             message=resp.NOT_FOUND)


    @poster_ns.expect(poster)
    def put(self, id: int):
        data = request.get_json()
        obj, err = poster_domain.update(db.session, data, id)
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


class PosterList(Resource):
    @posters_ns.doc('Get all the posters')
    def get(self):
        obj = poster_domain.read_all(db.session)
        if obj:
            return response_with(resp.SUCCESS_200, value=obj)
        return response_with(resp.NOT_FOUND_404,
                             message=resp.NOT_FOUND)

    @posters_ns.expect(poster)
    @posters_ns.doc('Create a poster')
    def post(self):
        data = request.get_json()
        obj, err = poster_domain.create(db.session, data)
        if err:
            return response_with(resp.INVALID_INPUT_422,
                                 message=resp.CANT_CREATE,
                                 value=err.errors())
        if obj:
            return response_with(resp.SUCCESS_201, value=obj)

        return response_with(resp.INVALID_INPUT_422,
                             message=resp.CANT_CREATE)
