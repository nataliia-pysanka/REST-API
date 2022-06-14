from flask import Blueprint, request
from flask_login import LoginManager, login_user, current_user, logout_user

from .util.responses import response_with
import app.util.responses as resp

from app.domain.user import DomainUser
from app.crud.user import CRUDUser

login_manager = LoginManager()
auth_routes = Blueprint('auth', __name__, url_prefix='/auth')

user_domain = DomainUser(CRUDUser())


@login_manager.user_loader
def load_user(user_id):
    return user_domain.get_model_by_id(id=user_id)


@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nickname = data.get('nickname', 'guest')
    password = data.get('password', '')
    user = user_domain.get_model_by_nickname(nickname)

    if user.verify_password(password):
        login_user(user)
        user_data = user_domain.get_dict_by_nickname(nickname)
        return response_with(resp.SUCCESS_200, value=user_data)
    else:
        return response_with(resp.UNAUTHORIZED_401)


@auth_routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    obj, err = user_domain.create(data)
    if err:
        return response_with(resp.INVALID_INPUT_422,
                             message=resp.CANT_CREATE,
                             value=err.errors())

    if user_domain.get_user_by_nickname(obj.nickname):
        return response_with(resp.ALREADY_EXIST_400)

    if obj:
        return response_with(resp.SUCCESS_201, value=obj)

    return response_with(resp.INVALID_INPUT_422,
                         message=resp.CANT_CREATE)


@auth_routes.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return response_with(resp.SUCCESS_200, message='Logout success')


@auth_routes.route('/user_info', methods=['POST'])
def user_info():
    if current_user.is_authenticated:
        user_data = user_domain.get_dict_by_model(current_user)
        return response_with(resp.SUCCESS_200, value={'user': user_data})
    else:
        return response_with(resp.UNAUTHORIZED_401)
