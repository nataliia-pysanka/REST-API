from flask import request
from flask_restx import Resource, fields, Namespace

from app.models.role import RoleModel
from app.schemas.role import RoleSchema
from app.CRUD.role import CRUDRole

from app.db import db

ROLE_NOT_FOUND = "Role not found."
ROLE_ALREADY_EXISTS = "Role '{}' already exists."

role_ns = Namespace('role', description='Item related operations')
roles_ns = Namespace('roles', description='Items related operations')

role_schema = RoleSchema()
role_list_schema = RoleSchema(many=True)
crud_role = CRUDRole(RoleModel)

role = roles_ns.model('Role', {
    'name': fields.String('Admin'),
    'description': fields.String('Could do anything'),
    'enabled': fields.Boolean(True)
})


class Role(Resource):
    def get(self, id: int):
        obj = crud_role.read(db.session, id)
        if obj:
            return role_schema.dump(obj), 200
        return {'message': ROLE_NOT_FOUND}, 404

    def delete(self, id: int):
        obj = crud_role.delete(db.session, id)
        if obj:
            return {'message': "Role deleted successfully"}, 200
        return {'message': ROLE_NOT_FOUND}, 404

    @role_ns.expect(role)
    def put(self, id: int):
        obj = crud_role.update(db.session, request.get_json(), id)
        if obj:
            return {'message': "Role updated successfully"}, 200
        return {'message': ROLE_NOT_FOUND}, 404


class RoleList(Resource):
    @role_ns.doc('Get all the roles')
    def get(self):
        obj = crud_role.read_all(db.session)
        if obj:
            return role_list_schema.dump(obj), 200
        return {'message': ROLE_NOT_FOUND}, 404

    @roles_ns.expect(role)
    @roles_ns.doc('Create a role')
    def post(self):
        role_json = request.get_json()
        role_data = role_schema.load(role_json)
        obj = crud_role.create(db.session, role_data)
        if obj:
            return role_schema.dump(role_data), 201
