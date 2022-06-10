from flask import Blueprint, request
from flask_login import LoginManager, login_user, current_user, logout_user
from flask import jsonify
from marshmallow.exceptions import ValidationError

from .util.responses import response_with
import app.util.responses as resp


from app.db import db
from app.domain.user import DomainUser
from app.schemas.user import UserSchema
from app.crud.user import CRUDUser

login_manager = LoginManager()
auth_routes = Blueprint('auth', __name__, url_prefix='/auth')

user_schema = UserSchema()
user_domain = DomainUser(CRUDUser())


@login_manager.user_loader
def load_user(user_id):
    return user_domain.read(id=user_id)


@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nickname = data.get('nickname', 'guest')
    password = data.get('password', '')

    user = user_domain.get_user_by_nickname(nickname)

    if user.verify_password(password):
        login_user(user)
        user_data = user_schema.dump(user)
        return response_with(resp.SUCCESS_200, value={'user': user_data})
    else:
        return response_with(resp.UNAUTHORIZED_401)


@auth_routes.route('/signup', methods=['POST'])
def signup():
    try:
        user = user_schema.load(request.get_json())
    except ValidationError:
        return response_with(resp.INVALID_INPUT_422)

    if user_domain.get_user_by_nickname(user.nickname):
        return response_with(resp.ALREADY_EXIST_400)

    user_data = user_schema.dump(user)
    result = user_domain.create(user_data)
    if result:
        return response_with(resp.SUCCESS_201,
                             value={"user": user_schema.dump(result)})
    return response_with(resp.INVALID_INPUT_422)


@auth_routes.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return response_with(resp.SUCCESS_200, message='Logout success')


@auth_routes.route('/user_info', methods=['POST'])
def user_info():
    if current_user.is_authenticated:
        user_data = user_schema.dump(current_user)
        return response_with(resp.SUCCESS_200, value={'user': user_data})
    else:
        return response_with(resp.UNAUTHORIZED_401)
