from flask import request
from flask_restx import Resource, fields, Namespace
from flask_login import login_required

import app.util.responses as resp
from app.util.responses import response_with
from app.crud.user import CRUDUser
from app.domain.user import DomainUser

from app.db import db

user_ns = Namespace('user', description='Item related operations')
users_ns = Namespace('users', description='Items related operations')

user_domain = DomainUser(CRUDUser())

user = users_ns.model('User', {
    'nickname': fields.String('NickName'),
    'password': fields.String('Password'),
    'name': fields.String('Name'),
    'surname': fields.String('Surname'),
    'date_birth': fields.Date,
    'date_registry': fields.Date,
    'id_role': fields.Integer
})


class User(Resource):
    def get(self, id):
        obj = user_domain.read(db.session, id)
        if obj:
            return response_with(resp.SUCCESS_200, value=obj)
        return response_with(resp.NOT_FOUND_404,
                             message=resp.NOT_FOUND)

    @login_required
    def delete(self, id):
        obj = user_domain.delete(db.session, id)
        if obj:
            return response_with(resp.SUCCESS_200,
                                 message=resp.WAS_DELETED,
                                 value=obj)
        return response_with(resp.NOT_FOUND_404,
                             message=resp.NOT_FOUND)

    @user_ns.expect(user)
    @login_required
    def put(self, id):
        data = request.get_json()
        obj, err = user_domain.update(db.session, data, id)
        if err:
            return response_with(resp.INVALID_INPUT_422,
                                 message=resp.CANT_UPDATE,
                                 value=err.errors())
        if obj:
            return response_with(resp.SUCCESS_201, message=resp.UPDATED,
                                 value=obj)

        return response_with(resp.NOT_FOUND_404,
                             message=resp.NOT_FOUND)


class UserList(Resource):
    @users_ns.doc('Get all the users')
    def get(self):
        obj = user_domain.read_all(db.session)
        if obj:
            return response_with(resp.SUCCESS_200, value=obj)
        return response_with(resp.NOT_FOUND_404,
                             message=resp.NOT_FOUND)

