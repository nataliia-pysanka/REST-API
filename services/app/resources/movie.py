from flask import request, jsonify
from flask_restx import Resource, fields, Namespace
from flask_login import login_required, current_user

from app.schemas.movie import MovieCreate, MovieUpdate
from app.crud.movie import CRUDMovie
from app.crud.user import CRUDUser
from app.domain.movie import DomainMovie
from app.domain.user import DomainUser

from app.util.responses import response_with
import app.util.responses as resp

from app.db import db

movie_ns = Namespace('movie', description='Item related operations')
movies_ns = Namespace('movies', description='Items related operations')

movie = movies_ns.model('Movie', {
    'title': fields.String('Name of the Movie'),
    'description': fields.String('Description of the Movie'),
    'date_release': fields.Date(),
    'rating': fields.Float(0.00),
    'id_genre': fields.Integer,
    'id_director': fields.Integer,
    'id_poster': fields.Integer,
    'id_user': fields.Integer
})

movie_domain = DomainMovie(CRUDMovie())
user_domain = DomainUser(CRUDUser())


class Movie(Resource):
    def get(self, id):
        obj = movie_domain.read(db.session, id)
        if obj:
            return response_with(resp.SUCCESS_200, value=obj)
        return response_with(resp.NOT_FOUND_404,
                             message=resp.NOT_FOUND)

    @login_required
    def delete(self, id):
        user = movie_domain.read(db.session, id)
        if not user:
            return response_with(resp.NOT_FOUND_404,
                                 message=resp.NOT_FOUND)

        user_id = user['user']['id']
        if current_user.id == user_id or current_user.is_admin():
            obj = movie_domain.delete(db.session, id)
            print('obj', obj)
            if obj:
                return response_with(resp.SUCCESS_200,
                                     message=resp.WAS_DELETED)
        else:
            return response_with(resp.UNAUTHORIZED_401,
                             message=resp.NO_RIGHTS)

    @movie_ns.expect(movie)
    @login_required
    def put(self, id):
        user_id = movie_domain.read(db.session, id).id_user
        if current_user.id == user_id or current_user.is_admin():
            data = request.get_json()
            obj, err = movie_domain.update(db.session, data, id)
            if err:
                return response_with(resp.INVALID_INPUT_422,
                                     message=resp.CANT_UPDATE,
                                     value=err.errors())
            if obj:
                return response_with(resp.SUCCESS_201, message=resp.UPDATED,
                                     value=obj)

            return response_with(resp.NOT_FOUND_404,
                                 message=resp.NOT_FOUND)
        else:
            return response_with(resp.UNAUTHORIZED_401,
                             message=resp.NO_RIGHTS)


class MovieList(Resource):
    # @movies_ns.doc('Get all the movies')
    # def get(self):
    #     obj = movie_domain.read_all()
    #     if obj:
    #         return response_with(resp.SUCCESS_200, value=obj)
    #     return response_with(resp.NOT_FOUND_404,
    #                          message=resp.NOT_FOUND)

    @movies_ns.doc('Get all the movies')
    def get(self):
        args = request.args

        json = movie_domain.get_movie_by_filter(db.session, args)

        if not json:
            return response_with(resp.NOT_FOUND_404,
                                 message="Movie not Found")
        offset = int(args.get('offset', '0'))
        limit = int(args.get('limit', '10'))

        query = request.full_path
        if query.find('offset=') == -1:
            query += f'&offset={offset}'
        if query.find('limit=') == -1:
            query += f'&limit={limit}'

        change_query = f'offset={offset}'

        if json:
            next_url = query.replace(change_query, f'offset={offset + limit}')
        else:
            next_url = ''

        if offset >= limit:
            prev_url = query.replace(change_query, f'offset={offset - limit}')
        else:
            prev_url = ''

        return jsonify({'prev_url': prev_url, 'next_url': next_url,
                        'result': json})

    @movies_ns.expect(movie)
    @movies_ns.doc('Create a movie')
    @login_required
    def post(self):
        data = request.get_json()
        # user = user_domain.get_dict_by_nickname('egepsihora')
        data['id_user'] = 1
        # data['nickname'] = user['nickname']
        # data['date_registry'] = user['date_registry']
        # data['id_role'] = user['id_role']

        obj, err = movie_domain.create(db.session, data)
        if err:
            return response_with(resp.INVALID_INPUT_422,
                                 message=resp.CANT_CREATE,
                                 value=err.errors())
        if obj:
            return response_with(resp.SUCCESS_201, value=obj)

        return response_with(resp.INVALID_INPUT_422,
                             message=resp.CANT_CREATE)
