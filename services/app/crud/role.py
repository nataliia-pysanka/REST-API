from sqlalchemy.orm import Session
from app.schemas.role import RoleSchema
from app.crud.base import CRUDBase
from app.models.role import RoleModel
from typing import Any, List


class CRUDRole(CRUDBase[RoleModel, RoleSchema]):
    def __init__(self):
        self.model = RoleModel

    def create(self, session: Session, obj_data: Any) -> RoleModel:
        db_obj = self.model(name=obj_data.name,
                            description=obj_data.description,
                            enabled=obj_data.enabled)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

