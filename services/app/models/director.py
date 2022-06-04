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

    def json(self):
        return {'name': self.name,
                'surname': self.surname,
                'date_birth': self.date_birth,
                'wiki_url': self.wiki_url
                }

    @classmethod
    def find_by_name(cls, name, surname):
        return cls.query.filter_by(name=name, surname=surname).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
