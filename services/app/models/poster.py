from app.db import db
from typing import List


class PosterModel(db.Model):
    __tablename__: str = 'poster'

    id = db.Column(db.INTEGER, primary_key=True)
    url = db.Column(db.VARCHAR)

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return "<PosterModel(url='%s')>" % (
            self.url)

    def json(self):
        return {'url': self.url}

    @classmethod
    def find_by_id(cls, _id) -> "PosterModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["PosterModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
