from flask import request
from flask_restx import Resource, fields, Namespace
from flask_login import login_required

from app.models.user import UserModel
from app.schemas.user import UserSchema
from app.crud.user import CRUDUser
from app.domain.user import DomainUser

from app.util.responses import response_with
import app.util.responses as resp

USER_NOT_FOUND = "User not found."
USER_ALREADY_EXISTS = "User '{}' already exists."

user_ns = Namespace('user', description='Item related operations')
users_ns = Namespace('users', description='Items related operations')

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

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
        obj = user_domain.read(id)
        if obj:
            return response_with(resp.SUCCESS_200,
                                 value={"user": user_schema.dump(obj)})
        return response_with(resp.NOT_FOUND_404,
                             message="User not Found")

    @login_required
    def delete(self, id):
        obj = user_domain.delete(id)
        if obj:
            return response_with(resp.SUCCESS_200,
                      value={"user": user_schema.dump(obj)},
                      message="User was deleted successfully")

        return response_with(resp.NOT_FOUND_404,
                             message="User not Found")

    @user_ns.expect(user)
    @login_required
    def put(self, id):
        obj = user_domain.update(request.get_json(), id)
        if obj:
            return {'message': "User updated successfully"}, 200
        return {'message': USER_NOT_FOUND}, 404


class UserList(Resource):
    @users_ns.doc('Get all the users')
    def get(self):
        obj = user_domain.read_all()
        if obj:
            return response_with(resp.SUCCESS_200,
                          value={"user": user_list_schema.dump(obj)})
        return response_with(resp.NOT_FOUND_404,
                          message="User not Found")

    @users_ns.expect(user)
    @users_ns.doc('Create a user')
    @login_required
    def post(self):
        try:
            user_json = request.get_json()
            obj = user_schema.load(user_json)
        except ValidationError:
            return response_with(resp.INVALID_INPUT_422)

        if user_domain.get_user_by_nickname(obj.nickname):
            return response_with(resp.ALREADY_EXIST_400)

        user_data = user_schema.dump(obj)
        obj = user_domain.create(user_data)
        if obj:
            return response_with(resp.SUCCESS_201,
                                 value={"user": user_schema.dump(obj)})
        return response_with(resp.INVALID_INPUT_422)
