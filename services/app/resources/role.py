from flask import request
from flask_restx import Resource, fields, Namespace

import app.util.responses as resp
from app.util.responses import response_with
from app.domain.role import DomainRole
from app.crud.role import CRUDRole

from app.db import db

role_ns = Namespace('role', description='Item related operations')
roles_ns = Namespace('roles', description='Items related operations')

role_domain = DomainRole(CRUDRole())

role = roles_ns.model('Role', {
    'name': fields.String('Admin'),
    'description': fields.String('Could do anything'),
    'enabled': fields.Boolean(True)
})


class Role(Resource):
    def get(self, id: int):
        obj = role_domain.read(db.session, id)
        if obj:
            return response_with(resp.SUCCESS_200, value=obj)
        return response_with(resp.NOT_FOUND_404,
                             message=resp.NOT_FOUND)

    def delete(self, id: int):
        obj = role_domain.delete(db.session, id)
        if obj:
            return response_with(resp.SUCCESS_200,
                                 message=resp.WAS_DELETED,
                                 value=obj)
        return response_with(resp.NOT_FOUND_404,
                             message=resp.NOT_FOUND)

    @role_ns.expect(role)
    def put(self, id: int):
        def put(self, id: int):
            data = request.get_json()
            obj, err = role_domain.update(db.session, data, id)
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


class RoleList(Resource):
    @roles_ns.doc('Get all the roles')
    def get(self):
        obj = role_domain.read_all(db.session)
        if obj:
            return response_with(resp.SUCCESS_200, value=obj)
        return response_with(resp.NOT_FOUND_404,
                             message=resp.NOT_FOUND)

    @roles_ns.expect(role)
    @roles_ns.doc('Create a role')
    def post(self):
        data = request.get_json()
        obj, err = role_domain.create(db.session, data)
        if err:
            return response_with(resp.INVALID_INPUT_422,
                                 message=resp.CANT_CREATE,
                                 value=err.errors())
        if obj:
            return response_with(resp.SUCCESS_201, value=obj)

        return response_with(resp.INVALID_INPUT_422,
                             message=resp.CANT_CREATE)
