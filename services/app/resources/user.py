from flask import request
from flask_restx import Resource, fields, Namespace
from flask_login import login_required

from app.models.user import UserModel
from app.schemas.user import UserSchema
from app.CRUD.user import CRUDUser

USER_NOT_FOUND = "User not found."
USER_ALREADY_EXISTS = "User '{}' already exists."

user_ns = Namespace('user', description='Item related operations')
users_ns = Namespace('users', description='Items related operations')

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

crud_user = CRUDUser(UserModel)

from app.db import db


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
        obj = crud_user.read(db.session, id)
        if obj:
            return user_schema.dump(obj), 200
        return {'message': USER_NOT_FOUND}, 404

    @login_required
    def delete(self, id):
        obj = crud_user.delete(db.session, id)
        if obj:
            return {'message': "User deleted successfully"}, 200
        return {'message': USER_NOT_FOUND}, 404

    @user_ns.expect(user)
    @login_required
    def put(self, id):
        obj = crud_user.update(db.session, request.get_json(), id)
        if obj:
            return {'message': "User updated successfully"}, 200
        return {'message': USER_NOT_FOUND}, 404


class UserList(Resource):
    @user_ns.doc('Get all the users')
    def get(self):
        obj = crud_user.read_all(db.session)
        print(obj)
        if obj:
            return user_list_schema.dump(obj), 200
        return {'message': USER_NOT_FOUND}, 404

    @users_ns.expect(user)
    @users_ns.doc('Create a user')
    @login_required
    def post(self):
        user_json = request.get_json()
        obj = user_schema.load(user_json)
        user_data = user_schema.dump(obj)
        obj = crud_user.create(db.session, user_data)
        if obj:
            return user_data, 201
