"""Module for sub-class CRUDUser"""
from typing import Any, List
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate
from app.crud.base import CRUDBase
from app.models.user import User


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """Class for CRUD operations with instance user"""
    def __init__(self):
        self.model = User

    def create(self, session: Session, obj_data: Any) -> User:
        """Creates object and save to session"""
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

    def get_id_by_name(self, session: Session, name: str) -> Any:
        """Returns id of object by name"""
        obj = session.query(self.model).filter(self.model.name.ilike(
            f'%{name}%')).first()
        if obj:
            return obj.id

    def read(self, session: Session, id: Any) -> User:
        """Reads object"""
        return session.query(self.model).get(id)

    def read_all(self, session: Session, skip: int = 0, limit: int = 10) \
            -> List[User]:
        """Reads all objects"""
        return session.query(self.model).offset(skip).limit(limit).all()

    def get_user_by_nickname(self, session: Session, nickname: str) \
            -> User:
        """Returns object by nickname"""
        obj = session.query(self.model).filter(self.model.nickname.ilike(
            f'%{nickname}%')).first()
        if obj:
            return obj
