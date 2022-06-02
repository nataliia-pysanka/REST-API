from flask import jsonify
from flask_restx import Resource
from app import api


@api.route('/hello')
class OK(Resource):
    def get(self):
        return jsonify(ok='OK')
