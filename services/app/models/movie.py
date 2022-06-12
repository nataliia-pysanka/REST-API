from app.db import db
from app.models.genre import Genre
from app.models.director import Director
from app.models.poster import Poster
from app.models.role import Role
from app.models.user import User


class Movie(db.Model):
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

# from sqlalchemy import Text, Float, Date, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship
#
# from app.db import Base
#
#
# class Movie(Base):
#     __tablename__: str = 'movies'
#     __table_args__ = {'extend_existing': True}
#
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, nullable=False)
#     description = Column(Text, default=None)
#     date_release = Column(Date, default=None)
#     rating = Column(Float(precision=2), default=None)
#
#     id_genre = Column(Integer, ForeignKey('genre.id'),
#                       nullable=True,
#                       default=None)
#     genre = relationship("Genre",
#                          back_populates="movies")
#
#     id_director = Column(Integer, ForeignKey('director.id'),
#                          nullable=True,
#                          default=None)
#     director = relationship("Director",
#                             back_populates="movies")
#
#     id_poster = Column(Integer, ForeignKey('poster.id'),
#                        nullable=True,
#                        default=None)
#     poster = relationship("Poster", back_populates="movies")
#
#     id_user = Column(Integer, ForeignKey('user.id'),
#                      nullable=False)
#     user = relationship("User",
#                         back_populates="movies")
