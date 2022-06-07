from flask import Flask, Blueprint, jsonify, request
from flask_migrate import Migrate
from flask_restx import Api
from marshmallow import ValidationError

import click


from .config import Config
from app.ma import ma
from app.db import db

from .resources.movie import Movie, MovieList, movie_ns, movies_ns
from .resources.user import User, UserList, user_ns, users_ns
from .resources.role import Role, RoleList, role_ns, roles_ns
from .resources.director import Director, DirectorList, director_ns, \
                                directors_ns
from .resources.genre import Genre, GenreList, genre_ns, genres_ns
from .resources.poster import Poster, PosterList, poster_ns, posters_ns

from .routes.movie import movie_routes

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)

api_resources = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_resources, doc='/doc', title='Sample Flask-RestPlus Application')
app.register_blueprint(api_resources)
app.register_blueprint(movie_routes)

api.add_namespace(movie_ns)
api.add_namespace(movies_ns)

api.add_namespace(user_ns)
api.add_namespace(users_ns)

api.add_namespace(role_ns)
api.add_namespace(roles_ns)

api.add_namespace(director_ns)
api.add_namespace(directors_ns)

api.add_namespace(genre_ns)
api.add_namespace(genres_ns)

api.add_namespace(poster_ns)
api.add_namespace(posters_ns)


@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


movie_ns.add_resource(Movie, '/<int:id>')
movies_ns.add_resource(MovieList, "")

user_ns.add_resource(User, '/<int:id>')
users_ns.add_resource(UserList, "")

role_ns.add_resource(Role, '/<int:id>')
roles_ns.add_resource(RoleList, "")

director_ns.add_resource(Director, '/<int:id>')
directors_ns.add_resource(DirectorList, "")

poster_ns.add_resource(Poster, '/<int:id>')
posters_ns.add_resource(PosterList, "")

genre_ns.add_resource(Genre, '/<int:id>')
genres_ns.add_resource(GenreList, "")


@app.cli.command("seed")
def seed():
    click.echo('Seed the database')
