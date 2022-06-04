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
