from app.db import db
from typing import List
from datetime import datetime
from app.models.role import Role

from app.config import ADMIN_ID


class User(db.Model):
    __tablename__: str = 'user'
    id = db.Column(db.INTEGER, primary_key=True)
    nickname = db.Column(db.VARCHAR, unique=True, nullable=False)
    password = db.Column(db.VARCHAR, nullable=False)
    name = db.Column(db.VARCHAR, nullable=True, default=None)
    surname = db.Column(db.VARCHAR, nullable=True, default=None)
    date_birth = db.Column(db.DATE, nullable=True, default=None)
    date_registry = db.Column(db.DATE, default=datetime)
    id_role = db.Column(db.INTEGER, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship("Role", )

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

    def verify_password(self, password):
        if self.password == password:
            return True
        return False

    def json(self):
        return {'nickname': self.nickname,
                'date_registry': self.date_registry}

    @staticmethod
    def is_authenticated(self):
        return True

    @staticmethod
    def is_active(self):
        return True

    @staticmethod
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def is_admin(self):
        if str(self.id_role) == ADMIN_ID:
            return True
        return False

