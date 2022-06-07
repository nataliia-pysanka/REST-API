from flask import Blueprint, request
from flask_login import LoginManager, login_user, current_user, logout_user
from flask import jsonify

from app.db import db
from app.models.user import UserModel
from app.schemas.user import UserSchema
from app.CRUD.user import CRUDUser

login_manager = LoginManager()

auth_routes = Blueprint('auth', __name__, url_prefix='/auth')


@login_manager.user_loader
def load_user(user_id):
    return CRUDUser(UserModel).read(db.session, id=user_id)


@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nickname = data.get('nickname', 'guest')
    password = data.get('password', '')

    user = CRUDUser(UserModel).get_user_by_nickname(db.session, nickname)
    if user.verify_password(password):
        login_user(user)
        return UserSchema().dump(user)
    else:
        return jsonify({"status": 401,
                        "reason": "Username or Password Error"})


@auth_routes.route('/signup', methods=['POST'])
def signup():
    try:
        user = UserSchema().load(request.get_json())
        user_data = UserSchema().dump(user)
        CRUDUser(UserModel).create(db.session, user_data)
        return jsonify({"status": 201,
                        "reason": "User was created"})
    except Exception as err:
        print(err)
        return jsonify({"status": 422,
                        "reason": "Can't create user"})


@auth_routes.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify(**{'result': 200,
                      'data': {'message': 'logout success'}})


@auth_routes.route('/user_info', methods=['POST'])
def user_info():
    if current_user.is_authenticated:
        resp = {"result": 200,
                "data": current_user.json()}
    else:
        resp = {"result": 401,
                "data": {"message": "user no login"}}
    return jsonify(**resp)
