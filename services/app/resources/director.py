"""Module for Director resources"""
from flask import request
from flask_restx import Resource, fields, Namespace

import app.util.responses as resp
from app.util.responses import response_with
from app.crud.director import CRUDDirector
from app.domain.director import DomainDirector

from app.db import db

director_ns = Namespace('director', description='Item related operations')
directors_ns = Namespace('directors', description='Items related operations')

director_domain = DomainDirector(CRUDDirector())

director = directors_ns.model('Director', {
    'name': fields.String('Christopher'),
    'surname': fields.String('Nolan'),
    'date_birth': fields.Date(),
    'wiki_url': fields.String('https://en.wikipedia.org/wiki/Christopher_Nolan')
})


class Director(Resource):
    """Class-resource for single instance Director"""
    def get(self, id: int):
        """GET method"""
        obj = director_domain.read(db.session, id)
        if obj:
            return response_with(resp.SUCCESS_200, value=obj)
        return response_with(resp.NOT_FOUND_404,
                             message=resp.NOT_FOUND)

    def delete(self, id: int):
        """DELETE method"""
        obj = director_domain.delete(db.session, id)
        if obj:
            return response_with(resp.SUCCESS_200,
                                 message=resp.WAS_DELETED,
                                 value=obj)
        return response_with(resp.NOT_FOUND_404,
                             message=resp.NOT_FOUND)

    @director_ns.expect(director)
    def put(self, id: int):
        """PUT method"""
        data = request.get_json()
        obj, err = director_domain.update(db.session, data, id)
        if err:
            return response_with(resp.INVALID_INPUT_422,
                                 message=resp.CANT_UPDATE,
                                 value=err.errors())
        if obj:
            return response_with(resp.SUCCESS_201, message=resp.UPDATED,
                                value=obj)

        return response_with(resp.NOT_FOUND_404,
                             message=resp.NOT_FOUND)


class DirectorList(Resource):
    """Class-resource for couple instances of Director"""
    @directors_ns.doc('Get all the directors')
    def get(self):
        """GET method"""
        obj = director_domain.read_all(db.session)
        if obj:
            return response_with(resp.SUCCESS_200, value=obj)
        return response_with(resp.NOT_FOUND_404,
                             message=resp.NOT_FOUND)

    @directors_ns.expect(director)
    @directors_ns.doc('Create a director')
    def post(self):
        """POST method"""
        data = request.get_json()
        obj, err = director_domain.create(db.session, data)
        if err:
            return response_with(resp.INVALID_INPUT_422,
                                 message=resp.CANT_CREATE,
                                 value=err.errors())
        if obj:
            return response_with(resp.SUCCESS_201, value=obj)

        return response_with(resp.INVALID_INPUT_422,
                             message=resp.CANT_CREATE)
