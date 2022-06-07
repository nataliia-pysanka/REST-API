from app.db import db
from typing import List
from app.models.genre import GenreModel
from app.models.director import DirectorModel
from app.models.poster import PosterModel
from app.models.role import RoleModel
from app.models.user import UserModel


class MovieModel(db.Model):
    __tablename__: str = 'movie'

    id = db.Column(db.INTEGER, primary_key=True, index=True)
    title = db.Column(db.VARCHAR, nullable=False)
    description = db.Column(db.TEXT)
    date_release = db.Column(db.DATE)
    rating = db.Column(db.Float(precision=2))

    id_genre = db.Column(db.INTEGER, db.ForeignKey('genre.id'), nullable=True,
                         default=None)
    genre = db.relationship("GenreModel", )

    id_director = db.Column(db.INTEGER, db.ForeignKey('director.id'),
                            nullable=True, default=None)
    director = db.relationship("DirectorModel", )

    id_poster = db.Column(db.INTEGER, db.ForeignKey('poster.id'), default=None)
    poster = db.relationship("PosterModel", )

    id_user = db.Column(db.INTEGER, db.ForeignKey('user.id'), nullable=False,
                        default=None)
    user = db.relationship("UserModel", )

    def __init__(self, title, description, date_release, rating,
                id_genre=None, id_director=None, id_poster=None, id_user=None):
        self.title = title
        self.description = description
        self.date_release = date_release
        self.rating = rating
        self.id_genre = id_genre
        self.id_director = id_director
        self.id_poster = id_poster
        self.id_user = id_user

    def __repr__(self):
        return "<Movie(title='%s', rating='%s', date_release='%s')>" % (
            self.title, self.rating, self.date_release)
