from app.db import db
from typing import List
from datetime import datetime
from app.models.role import RoleModel


class UserModel(db.Model):
    __tablename__: str = 'user'
    id = db.Column(db.INTEGER, primary_key=True)
    nickname = db.Column(db.VARCHAR, unique=True, nullable=False)
    password = db.Column(db.VARCHAR, nullable=False)
    name = db.Column(db.VARCHAR)
    surname = db.Column(db.VARCHAR)
    date_birth = db.Column(db.DATE)
    date_registry = db.Column(db.DATE, default=datetime)

    id_role = db.Column(db.INTEGER, db.ForeignKey('role.id'))
    role = db.relationship("RoleModel", )

    def __init__(self, nickname, password, name, surname, date_birth,
                 date_registry, id_role):
        self.nickname = nickname
        self.password = password
        self.name = name
        self.surname = surname
        self.date_birth = date_birth
        self.date_registry = date_registry
        self.id_role = id_role

    def __repr__(self):
        return 'UserModel(nickname=%s, date_registry=%s)' % (
            self.nickname, self.date_registry)

    def json(self):
        return {'nickname': self.nickname, 'date_registry': self.date_registry}

    @classmethod
    def find_by_nickname(cls, nickname) -> "UserModel":
        return cls.query.filter_by(nickname=nickname).first()

    @classmethod
    def find_by_id(cls, _id) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
