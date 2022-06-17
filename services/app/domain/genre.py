"""Module for domain class Genre"""
from typing import Any, List, Optional, Dict, Union, Tuple
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.domain.base import DomainBase
from app.schemas.genre import GenreCreate, GenreUpdate, GenreDB
from app.models.genre import Genre

from app.util.log import logger


class DomainGenre(DomainBase):
    """Class for connecting data layer with routes/resources for instance
        genre"""
    def get_id_by_name(self, session: Session, name_list: List[str]) \
            -> List[Genre]:
        """Reads object by its name and returns it"""
        if name_list:
            return self.crud.get_id_by_name(session, name_list)
        return []

    def read(self, session: Session, id: Any) -> Optional[Genre]:
        """Reads object and returns like dict"""
        query = super(DomainGenre, self).read(session, id)
        if query:
            return GenreDB.from_orm(query).dict()
        return None

    def read_all(self, session: Session) -> List[Optional[Dict]]:
        """Reads all objects and returns like list of dict"""
        query = super(DomainGenre, self).read_all(session)
        lst = []
        for obj in query:
            lst.append(GenreDB.from_orm(obj).dict())
        return lst

    def create(self, session: Session, obj_data: Dict) \
            -> Union[Tuple[None, ValidationError],
                     Tuple[Dict, None],
                     Tuple[None, None]]:
        """Parses data, creates object and returns like dict"""
        try:
            data = GenreCreate.parse_obj(obj_data)
        except ValidationError as err:
            logger.error(err.raw_errors)
            return None, err

        query = super(DomainGenre, self).create(session, data)
        if query:
            return GenreDB.from_orm(query).dict(), None
        return None, None

    def update(self, session: Session, obj_data: Dict, id: Any) ->\
            Union[Tuple[None, ValidationError],
                  Tuple[Dict, None],
                  Tuple[None, None]]:
        """Parses data, updates object and returns like dict"""
        query = super(DomainGenre, self).read(session, id)
        if not query:
            return None, None

        obj = GenreDB.from_orm(query)
        obj_dict = obj.dict()

        for field in obj_dict:
            if field not in obj_dict:
                obj_data.update({field: obj_dict[field]})

        try:
            data = GenreUpdate.parse_obj(obj_data)
        except ValidationError as err:
            logger.error(err.raw_errors)
            return None, err

        query = super(DomainGenre, self).update(session, query, data)
        if query:
            return GenreDB.from_orm(query).dict(), None
        return None, None

    def delete(self, session: Session, id: Any) -> Optional[Dict]:
        """Deletes object and returns like dict"""
        query = super(DomainGenre, self).delete(session, id)
        if not query:
            return None
        return GenreDB.from_orm(query).dict()
