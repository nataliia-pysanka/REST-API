"""Module for user authorization"""
from flask import Blueprint, request
from flask_login import LoginManager, login_user, current_user, logout_user

from .util.responses import response_with
import app.util.responses as resp

from app.domain.user import DomainUser
from app.crud.user import CRUDUser
from app.db import db

login_manager = LoginManager()
auth_routes = Blueprint('auth', __name__, url_prefix='/auth')

user_domain = DomainUser(CRUDUser())


@login_manager.user_loader
def load_user(user_id):
    """Loads current user"""
    return user_domain.get_model_by_id(db.session, id=user_id)


@auth_routes.route('/login', methods=['POST'])
def login():
    """Makes login"""
    data = request.get_json()
    nickname = data.get('nickname', 'guest')
    password = data.get('password', '')
    user = user_domain.get_model_by_nickname(db.session, nickname)
    if user and user.verify_password(password):
        login_user(user)
        user_data = user_domain.get_dict_by_nickname(db.session, nickname)
        return response_with(resp.SUCCESS_200, value=user_data)
    else:
        return response_with(resp.USER_NOT_FOUND_404)


@auth_routes.route('/signup', methods=['POST'])
def signup():
    """Creates new user"""
    data = request.get_json()
    obj, err = user_domain.create(db.session, data)
    if err:
        return response_with(resp.INVALID_INPUT_422,
                             message=resp.CANT_CREATE,
                             value=err.errors())

    if user_domain.get_model_by_nickname(db.session, obj.nickname):
        return response_with(resp.ALREADY_EXIST_400)

    if obj:
        return response_with(resp.SUCCESS_201, value=obj)

    return response_with(resp.INVALID_INPUT_422,
                         message=resp.CANT_CREATE)


@auth_routes.route('/logout', methods=['POST'])
def logout():
    """Makes logout"""
    logout_user()
    return response_with(resp.SUCCESS_200, message='Logout success')


@auth_routes.route('/user_info', methods=['POST'])
def user_info():
    """Returns info about current user"""
    if current_user.is_authenticated:
        user_data = user_domain.get_dict_by_model(db.session, current_user)
        return response_with(resp.SUCCESS_200, value={'user': user_data})

    return response_with(resp.UNAUTHORIZED_401)
