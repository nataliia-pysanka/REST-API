"""Module for sub-class CRUDRole"""
from typing import Any
from sqlalchemy.orm import Session
from app.schemas.role import RoleCreate, RoleUpdate
from app.crud.base import CRUDBase
from app.models.role import Role


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    """Class for CRUD operations with instance role"""
    def __init__(self):
        self.model = Role

    def create(self, session: Session, obj_data: Any) -> Role:
        """Creates object and save to session"""
        db_obj = self.model(name=obj_data.name,
                            description=obj_data.description,
                            enabled=obj_data.enabled)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

