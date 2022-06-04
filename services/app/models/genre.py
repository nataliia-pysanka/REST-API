from app.db import db
from typing import List


class GenreModel(db.Model):
    __tablename__: str = 'genre'

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<GenreModel(name='%s')>" % (
            self.name)

    def json(self):
        return {'name': self.name}

    @classmethod
    def find_by_name(cls, name) -> "GenreModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id) -> "GenreModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["GenreModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
