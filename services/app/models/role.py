from app.db import db
from typing import List


class RoleModel(db.Model):
    __tablename__: str = 'role'

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR, nullable=False)
    description = db.Column(db.TEXT)
    enabled = db.Column(db.BOOLEAN, default=True)

    def __init__(self, name, description, enabled):
        self.name = name
        self.description = description
        self.enabled = enabled

    def __repr__(self):
        return "<RoleModel(name='%s', enabled='%s')>" % (
            self.name, self.enabled)

    def json(self):
        return {'name': self.name,
                'description': self.description,
                'enabled': self.enabled}

    @classmethod
    def find_by_name(cls, name) -> "RoleModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id) -> "RoleModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["RoleModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
