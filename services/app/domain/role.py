from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.domain.base import DomainBase
from app.schemas.role import RoleCreate, RoleUpdate, RoleDB
from typing import Any, List
from app.util.log import logger


class DomainRole(DomainBase):
    def get_id_by_name(self, name_list: List[str]) -> List[Any]:
        if name_list:
            return self.crud.get_id_by_name(Session, name_list)
        return []

    def read(self, id: Any):
        query = super(DomainRole, self).read(id)
        if query:
            return RoleDB.from_orm(query).dict()
        return None

    def read_all(self):
        query = super(DomainRole, self).read_all()
        lst = []
        for obj in query:
            lst.append(RoleDB.from_orm(obj).dict())
        return lst

    def create(self, obj_data: Any):
        try:
            data = RoleCreate.parse_obj(obj_data)
        except ValidationError as err:
            logger.error(err.raw_errors)
            return None, err

        query = super(DomainRole, self).create(data)
        if query:
            return RoleDB.from_orm(query).dict(), None
        return None, None

    def update(self, obj_data: Any, id: Any):
        query = super(DomainRole, self).read(id)
        if not query:
            return None, None

        obj = RoleDB.from_orm(query)
        obj_dict = obj.dict()

        for field in obj_dict:
            if field not in obj_dict:
                obj_data.update({field: obj_dict[field]})

        try:
            data = RoleUpdate.parse_obj(obj_data)
        except ValidationError as err:
            logger.error(err.raw_errors)
            return None, err

        query = super(DomainRole, self).update(query, data)
        if query:
            return RoleDB.from_orm(query).dict(), None
        return None, None

    def delete(self, id: Any):
        query = super(DomainRole, self).delete(id)
        if not query:
            return None
        return RoleDB.from_orm(query).dict()