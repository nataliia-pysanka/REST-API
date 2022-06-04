from sqlalchemy.orm import Session
from app.schemas.user import UserSchema
from app.CRUD.base import CRUDBase
from app.models.user import UserModel
from typing import Any, List


class CRUDUser(CRUDBase[UserModel, UserSchema]):
    def create(self, session: Session, obj_data: Any) -> UserModel:
        db_obj = self.model(nickname=obj_data.nickname,
                            password=obj_data.password,
                            name=obj_data.name,
                            surname=obj_data.surname,
                            date_birth=obj_data.date_birth,
                            date_registry=obj_data.date_registry,
                            id_role=obj_data.id_role)

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj
