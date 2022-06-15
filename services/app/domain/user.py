from sqlalchemy.orm import Session
from pydantic import ValidationError
from typing import Any, List
from app.domain.base import DomainBase
from app.schemas.user import UserCreate, UserUpdate, UserDB
from app.models.user import User
from app.util.log import logger


class DomainUser(DomainBase):
    def get_model_by_nickname(self, session: Session, nickname: str):
        model = self.crud.get_user_by_nickname(session, nickname)
        if model:
            return model
        return None

    def get_model_by_id(self, session: Session, id: Any):
        model = super(DomainUser, self).read(session, id)
        if model:
            return model
        return None

    def get_dict_by_id(self, session: Session, id: Any):
        model = super(DomainUser, self).read(session, id)
        if model:
            return UserDB.from_orm(model).dict()
        return None

    def get_dict_by_nickname(self, session: Session, nickname: str):
        model = self.crud.get_user_by_nickname(session, nickname)
        if model:
            return UserDB.from_orm(model).dict()
        return None

    def get_dict_by_model(self, model: User):
        if isinstance(model, User):
            return UserDB.from_orm(model).dict()
        return None

    def read(self, session: Session, id: Any):
        query = super(DomainUser, self).read(session, id)
        if query:
            return UserDB.from_orm(query).dict()
        return None

    def read_all(self, session: Session):
        query = super(DomainUser, self).read_all(session)
        lst = []
        for obj in query:
            lst.append(UserDB.from_orm(obj).dict())
        return lst

    def create(self, session: Session, obj_data: Any):
        try:
            data = UserCreate.parse_obj(obj_data)
        except ValidationError as err:
            logger.error(err.raw_errors)
            return None, err

        query = super(DomainUser, self).create(session, data)
        if query:
            return UserDB.from_orm(query).dict(), None
        return None, None

    def update(self, session: Session, obj_data: Any, id: Any):
        query = super(DomainUser, self).read(session, id)
        if not query:
            return None, None

        obj = UserDB.from_orm(query)
        obj_dict = obj.dict()

        for field in obj_dict:
            if field not in obj_dict:
                obj_data.update({field: obj_dict[field]})

        try:
            data = UserUpdate.parse_obj(obj_data)
        except ValidationError as err:
            logger.error(err.raw_errors)
            return None, err

        query = super(DomainUser, self).update(session, query, data)
        if query:
            return UserDB.from_orm(query).dict(), None
        return None, None

    def delete(self, session: Session, id: Any):
        query = super(DomainUser, self).delete(session, id)
        if not query:
            return None
        return UserDB.from_orm(query).dict()
