"""Module for describing table Genre"""
from app.db import db
from app.models.genre import Genre
from app.models.director import Director
from app.models.poster import Poster
from app.models.role import Role
from app.models.user import User


class Movie(db.Model):
    """Table movie"""
    __tablename__: str = 'movie'

    id = db.Column(db.INTEGER, primary_key=True, index=True)
    title = db.Column(db.VARCHAR, nullable=False)
    description = db.Column(db.TEXT, nullable=True, default=None)
    date_release = db.Column(db.DATE, nullable=True, default=None)
    rating = db.Column(db.Float(precision=2), nullable=True, default=None)

    id_genre = db.Column(db.INTEGER, db.ForeignKey('genre.id'), nullable=True,
                         default=None)
    genre = db.relationship("Genre", )

    id_director = db.Column(db.INTEGER, db.ForeignKey('director.id'),
                            nullable=True, default=None)
    director = db.relationship("Director", )

    id_poster = db.Column(db.INTEGER, db.ForeignKey('poster.id'), default=None)
    poster = db.relationship("Poster", )

    id_user = db.Column(db.INTEGER, db.ForeignKey('user.id'), nullable=False,
                        default=None)
    user = db.relationship("User", )

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
