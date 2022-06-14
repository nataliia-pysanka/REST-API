"""Module for base class for logical operations"""
from typing import Dict, Any
from app.crud.base import CRUDAbstract
from sqlalchemy.orm import Session


class DomainBase:
    """Class for connecting data layer with routes/resources"""
    def __init__(self, crud: CRUDAbstract):
        self.crud = crud

    def create(self, session: Session, obj_data: Any):
        """Calls crud operation create"""
        return self.crud.create(session, obj_data)

    def read(self, session: Session, id: Any):
        """Calls crud operation read"""
        return self.crud.read(session, id)

    def read_all(self, session: Session):
        """Calls crud operation read all"""
        return self.crud.read_all(session)

    def update(self, session: Session, obj_data: Any, id: Any):
        """Calls crud operation update"""
        return self.crud.update(session, obj_data, id)

    def delete(self, session: Session, id: Any):
        """Calls crud operation delete"""
        return self.crud.delete(session, id)
