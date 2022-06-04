from flask import request
from flask_restx import Resource, fields, Namespace

from app.models.user import UserModel
from app.schemas.user import UserSchema

USER_NOT_FOUND = "User not found."
USER_ALREADY_EXISTS = "User '{}' already exists."

user_ns = Namespace('user', description='Item related operations')
users_ns = Namespace('users', description='Items related operations')

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)


user = users_ns.model('User', {
    'nickname': fields.String('NickName'),
    'password': fields.String('Password'),
    'name': fields.String('Name'),
    'surname': fields.String('Surname'),
    'date_birth': fields.Date,
    'date_registry': fields.Date
})


class User(Resource):
    def get(self, _id):
        user_data = UserModel.find_by_id(_id)
        if user_data:
            return user_schema.dump(user_data)
        return {'message': USER_NOT_FOUND}, 404

    def delete(self, _id):
        user_data = UserModel.find_by_id(_id)
        if user_data:
            user_data.delete_from_db()
            return {'message': "User deleted successfully"}, 200
        return {'message': USER_NOT_FOUND}, 404

    @user_ns.expect(user)
    def put(self, _id):
        user_data = UserModel.find_by_id(_id)
        user_json = request.get_json()

        if user_data:
            user_data.nickname = user_json['nickname']
            user_data.password = user_json['password']
            user_data.name = user_json['name']
            user_data.surname = user_json['surname']
            user_data.date_birth = user_json['date_birth']
            user_data.date_registry = user_json['date_registry']
        else:
            user_data = user_schema.load(user_json)

        user_data.save_to_db()
        return user_schema.dump(user_data), 200


class UserList(Resource):
    @user_ns.doc('Get all users')
    def get(self):
        return user_list_schema.dump(UserModel.find_all()), 200

    @users_ns.expect(user)
    @users_ns.doc('Create a movie')
    def post(self):
        user_json = request.get_json()
        user_data = user_schema.load(user_json)
        user_data.save_to_db()

        return user_schema.dump(user_data), 201
