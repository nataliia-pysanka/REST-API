from sqlalchemy.orm import Session
from app.schemas.user import UserSchema
from app.CRUD.base import CRUDBase
from app.models.user import UserModel
from typing import Any, List


class CRUDUser(CRUDBase[UserModel, UserSchema]):
    def create(self, session: Session, obj_data: Any) -> UserModel:
        db_obj = self.model(nickname=obj_data['nickname'],
                            password=obj_data['password'],
                            name=obj_data['name'],
                            surname=obj_data['surname'],
                            date_birth=obj_data['date_birth'],
                            date_registry=obj_data['date_registry'],
                            id_role=obj_data['id_role'])
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def get_id_by_name(self, session: Session, name: str) -> Any:
        obj = session.query(self.model).filter(self.model.name.ilike(
            f'%{name}%')).first()
        if obj:
            return obj.id

    def read(self, session: Session, id: Any) -> UserModel:
        return session.query(self.model).get(id)

    def get_user_by_nickname(self, session: Session, nickname: str) \
            -> UserModel:
        obj = session.query(self.model).filter(self.model.nickname.ilike(
            f'%{nickname}%')).first()
        if obj:
            return obj
        return None
