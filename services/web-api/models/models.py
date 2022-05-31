from . import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Director(db.Model):
    __tablename__: str = 'director'
    id = db.Column(db.INTEGER, primary_key=True, index=True)
    name = db.Column(db.VARCHAR)
    surname = db.Column(db.VARCHAR)
    date_birth = db.Column(db.DATE)
    wiki_url = db.Column(db.VARCHAR)

    def __repr__(self):
        return "<Director(name='%s', surname='%s')>" % (
            self.name, self.surname)


class Genre(db.Model):
    __tablename__: str = 'genre'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR)

    def __repr__(self):
        return "<Genre(name='%s')>" % (
            self.name)


class Movie(db.Model):
    __tablename__: str = 'movie'
    id = db.Column(db.INTEGER, primary_key=True, index=True)
    title = db.Column(db.VARCHAR)
    description = db.Column(db.TEXT)
    date_release = db.Column(db.DATE)
    rating = db.Column(db.NUMERIC)

    id_director = db.Column(db.INTEGER, ForeignKey('director.id'))
    director = relationship("Director", back_populates="movie")

    id_poster = db.Column(db.INTEGER, ForeignKey('poster.id'))
    poster = relationship("Poster", back_populates="movie")

    id_user = db.Column(db.INTEGER, ForeignKey('user.id'))
    user = relationship("User", back_populates="movie")

    def __repr__(self):
        return "<Movie(title='%s', rating='%s', date_release='%s')>" % (
            self.title, self.rating, self.date_release)


class Poster(db.Model):
    __tablename__: str = 'poster'
    id = db.Column(db.INTEGER, primary_key=True)
    url = db.Column(db.VARCHAR)

    def __repr__(self):
        return "<Poster(url='%s')>" % (
            self.url)


class Role(db.Model):
    __tablename__: str = 'role'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR)
    description = db.Column(db.TEXT)
    enabled = db.Column(db.BOOLEAN)

    def __repr__(self):
        return "<Role(name='%s', enabled='%s')>" % (
            self.name, self.enabled)


class User(db.Model):
    __tablename__: str = 'user'
    id = db.Column(db.INTEGER, primary_key=True)
    nickname = db.Column(db.VARCHAR, unique=True, nullable=False)
    password = db.Column(db.VARCHAR, nullable=False)
    name = db.Column(db.VARCHAR)
    surname = db.Column(db.VARCHAR)
    date_birth = db.Column(db.DATE)
    date_registry = db.Column(db.DATE)

    id_role = db.Column(db.INTEGER, ForeignKey('role.id'))
    role = relationship("Role", back_populates="user")
