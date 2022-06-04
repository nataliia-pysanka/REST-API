from flask import request
from flask_restx import Resource, fields, Namespace

from app.models.role import RoleModel
from app.schemas.role import RoleSchema

ROLE_NOT_FOUND = "Role not found."
ROLE_ALREADY_EXISTS = "Role '{}' already exists."

role_ns = Namespace('role', description='Item related operations')
roles_ns = Namespace('roles', description='Items related operations')

role_schema = RoleSchema()
role_list_schema = RoleSchema(many=True)


role = roles_ns.model('Role', {
    'name': fields.String('Admin'),
    'description': fields.String('Could do anything'),
    'enabled': fields.Boolean(True)
})


class Role(Resource):
    def get(self, _id):
        role_data = RoleModel.find_by_id(_id)
        if role_data:
            return role_schema.dump(role_data)
        return {'message': ROLE_NOT_FOUND}, 404

    def delete(self, _id):
        role_data = RoleModel.find_by_id(_id)
        if role_data:
            role_data.delete_from_db()
            return {'message': "Role deleted successfully"}, 200
        return {'message': ROLE_NOT_FOUND}, 404

    @role_ns.expect(role)
    def put(self, _id):
        role_data = RoleModel.find_by_id(_id)
        role_json = request.get_json()

        if role_data:
            role_data.name = role_json['name']
            role_data.description = role_json['description']
            role_data.enabled = role_json['enabled']
        else:
            role_data = role_schema.load(role_json)

        role_data.save_to_db()
        return role_schema.dump(role_data), 200


class RoleList(Resource):
    @role_ns.doc('Get all roles')
    def get(self):
        return role_list_schema.dump(RoleModel.find_all()), 200

    @roles_ns.expect(role)
    @roles_ns.doc('Create a role')
    def post(self):
        role_json = request.get_json()
        role_data = role_schema.load(role_json)
        role_data.save_to_db()

        return role_schema.dump(role_data), 201
