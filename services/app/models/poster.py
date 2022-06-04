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
