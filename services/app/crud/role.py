from sqlalchemy.orm import Session
from app.schemas.role import RoleCreate, RoleUpdate
from app.crud.base import CRUDBase
from app.models.role import Role
from typing import Any


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def __init__(self):
        self.model = Role

    def create(self, session: Session, obj_data: Any) -> Role:
        db_obj = self.model(name=obj_data.name,
                            description=obj_data.description,
                            enabled=obj_data.enabled)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

