"""Module for domain class Director"""
from typing import Any, List, Dict, Optional, Union, Tuple
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.domain.base import DomainBase
from app.schemas.user import UserCreate, UserUpdate, UserDB
from app.models.user import User
from app.util.log import logger


class DomainUser(DomainBase):
    """Class for connecting data layer with routes/resources for instance
        user"""
    def get_model_by_nickname(self, session: Session, nickname: str) \
            -> Optional[User]:
        """Returns model by nickname"""

        model = self.crud.get_user_by_nickname(session, nickname)
        if model:
            return model
        return None

    def get_model_by_id(self, session: Session, id: Any) \
            -> Optional[User]:
        """Returns model by id"""
        model = super(DomainUser, self).read(session, id)
        if model:
            return model
        return None

    def get_dict_by_id(self, session: Session, id: Any) \
            -> Optional[Dict]:
        """Returns model by id like dictionary"""
        model = super(DomainUser, self).read(session, id)
        if model:
            return UserDB.from_orm(model).dict()
        return None

    def get_dict_by_nickname(self, session: Session, nickname: str) \
            -> Optional[Dict]:
        """Returns model by nickname like dictionary"""
        model = self.crud.get_user_by_nickname(session, nickname)
        if model:
            return UserDB.from_orm(model).dict()
        return None

    def get_dict_by_model(self, session: Session, model: User) \
            -> Optional[Dict]:
        """Returns model of inputted object"""
        if isinstance(model, User):
            return UserDB.from_orm(model).dict()
        return None

    def read(self, session: Session, id: Any) -> Optional[Dict]:
        """Reads object and returns like dict"""
        query = super(DomainUser, self).read(session, id)
        if query:
            return UserDB.from_orm(query).dict()
        return None

    def read_all(self, session: Session) -> List[Optional[Dict]]:
        """Reads all objects and returns like list of dict"""
        query = super(DomainUser, self).read_all(session)
        lst = []
        for obj in query:
            lst.append(UserDB.from_orm(obj).dict())
        return lst

    def create(self, session: Session, obj_data: Any) -> \
            Union[Tuple[None, ValidationError],
                  Tuple[Dict, None],
                  Tuple[None, None]]:
        """Parses data, creates object and returns like dict"""
        try:
            data = UserCreate.parse_obj(obj_data)
        except ValidationError as err:
            logger.error(err.raw_errors)
            return None, err

        query = super(DomainUser, self).create(session, data)
        if query:
            return UserDB.from_orm(query).dict(), None
        return None, None

    def update(self, session: Session, obj_data: Any, id: Any) ->\
            Union[Tuple[None, ValidationError],
                  Tuple[Dict, None],
                  Tuple[None, None]]:
        """Parses data, updates object and returns like dict"""
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

    def delete(self, session: Session, id: Any) -> Optional[Dict]:
        """Deletes object and returns like dict"""
        query = super(DomainUser, self).delete(session, id)
        if not query:
            return None
        return UserDB.from_orm(query).dict()

