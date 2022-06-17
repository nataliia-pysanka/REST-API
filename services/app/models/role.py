"""Module for describing table Role"""
from app.db import db


class Role(db.Model):
    """Table role"""
    __tablename__: str = 'role'

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR, nullable=False)
    description = db.Column(db.TEXT, nullable=True, default=None)
    enabled = db.Column(db.BOOLEAN, default=True)

    def __init__(self, name, description, enabled):
        self.name = name
        self.description = description
        self.enabled = enabled

    def __repr__(self):
        return "<RoleModel(name='%s', enabled='%s')>" % (
            self.name, self.enabled)

# from sqlalchemy import Boolean, Column, ForeignKey, Text, Integer, String, Date
# from sqlalchemy.orm import relationship
# from datetime import datetime
#
# from app.db import Base
#
#
# class Role(Base):
#     __tablename__: str = 'roles'
#     __table_args__ = {'extend_existing': True}
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     description = Column(Text, nullable=True, default=None)
#     enabled = Column(Boolean, default=True)
#
#     users = relationship("User", back_populates="role")
