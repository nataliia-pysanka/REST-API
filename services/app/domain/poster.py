from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.domain.base import DomainBase
from app.schemas.poster import PosterCreate, PosterUpdate, PosterDB
from typing import Any, List
from app.util.log import logger


class DomainPoster(DomainBase):
    def get_id_by_name(self, session: Session, name_list: List[str]) -> List[Any]:
        if name_list:
            return self.crud.get_id_by_name(session, name_list)
        return []

    def read(self, session: Session, id: Any):
        query = super(DomainPoster, self).read(session, id)
        if query:
            return PosterDB.from_orm(query).dict()
        return None

    def read_all(self, session: Session):
        query = super(DomainPoster, self).read_all(session)
        lst = []
        for obj in query:
            lst.append(PosterDB.from_orm(obj).dict())
        return lst

    def create(self, session: Session, obj_data: Any):
        try:
            data = PosterCreate.parse_obj(obj_data)
        except ValidationError as err:
            logger.error(err.raw_errors)
            return None, err

        query = super(DomainPoster, self).create(session, data)
        if query:
            return PosterDB.from_orm(query).dict(), None
        return None, None

    def update(self, session: Session, obj_data: Any, id: Any):
        query = super(DomainPoster, self).read(session, id)
        if not query:
            return None, None

        obj = PosterDB.from_orm(query)
        obj_dict = obj.dict()

        for field in obj_dict:
            if field not in obj_dict:
                obj_data.update({field: obj_dict[field]})

        try:
            data = PosterUpdate.parse_obj(obj_data)
        except ValidationError as err:
            logger.error(err.raw_errors)
            return None, err

        query = super(DomainPoster, self).update(session, query, data)
        if query:
            return PosterDB.from_orm(query).dict(), None
        return None, None

    def delete(self, session: Session, id: Any):
        query = super(DomainPoster, self).delete(session, id)
        if not query:
            return None
        return PosterDB.from_orm(query).dict()