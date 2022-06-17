"""Module for describing table Genre"""
from app.db import db


class Genre(db.Model):
    """Table genre"""
    __tablename__: str = 'genre'

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<GenreModel(name='%s')>" % (
            self.name)
