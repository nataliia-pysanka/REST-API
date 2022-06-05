from app.db import db
from typing import List


class DirectorModel(db.Model):
    __tablename__: str = 'director'

    id = db.Column(db.INTEGER, primary_key=True, index=True)
    name = db.Column(db.VARCHAR, nullable=False)
    surname = db.Column(db.VARCHAR, nullable=False)
    date_birth = db.Column(db.DATE)
    wiki_url = db.Column(db.VARCHAR)

    def __init__(self, name, surname, date_birth, wiki_url):
        self.name = name
        self.surname = surname
        self.date_birth = date_birth
        self.wiki_url = wiki_url

    def __repr__(self):
        return "<DirectorModel(name='%s', surname='%s')>" % (
            self.name, self.surname)
