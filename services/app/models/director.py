"""Module for describing table Director"""
from app.db import db


class Director(db.Model):
    """Table director"""
    __tablename__: str = 'director'

    id = db.Column(db.INTEGER, primary_key=True, index=True)
    name = db.Column(db.VARCHAR, nullable=False)
    surname = db.Column(db.VARCHAR, nullable=False)
    date_birth = db.Column(db.DATE, nullable=True, default=None)
    wiki_url = db.Column(db.VARCHAR, nullable=True, default=None)

    def __init__(self, name, surname, date_birth, wiki_url):
        self.name = name
        self.surname = surname
        self.date_birth = date_birth
        self.wiki_url = wiki_url

    def __repr__(self):
        return "<DirectorModel(name='%s', surname='%s')>" % (
            self.name, self.surname)
