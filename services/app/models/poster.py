from app.db import db


class Poster(db.Model):
    __tablename__: str = 'poster'

    id = db.Column(db.INTEGER, primary_key=True)
    url = db.Column(db.VARCHAR)

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return "<PosterModel(url='%s')>" % (
            self.url)

# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship
#
# from app.db import Base
#
#
# class Poster(Base):
#     __tablename__: str = 'posters'
#     __table_args__ = {'extend_existing': True}
#
#     id = Column(Integer, primary_key=True)
#     url = Column(String)
#
#     movies = relationship("Movie", back_populates="poster")

