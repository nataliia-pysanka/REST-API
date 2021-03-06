"""Module for sub-class CRUDGenre"""
from typing import Any, List
from sqlalchemy.orm import Session
from app.schemas.genre import GenreCreate, GenreUpdate
from app.crud.base import CRUDBase
from app.models.genre import Genre


class CRUDGenre(CRUDBase[Genre, GenreCreate, GenreUpdate]):
    """Class for CRUD operations with instance genre"""
    def __init__(self):
        self.model = Genre

    def create(self, session: Session, obj_data: Any) -> Genre:
        """Creates object and save to session"""
        db_obj = self.model(name=obj_data.name)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def get_id_by_name(self, session: Session, name_list: List[str]) \
            -> List[Any]:
        """Returns id of object by filter"""
        obj_all = []
        for name in name_list:
            query = session.query(self.model).filter(self.model.name.ilike(
                    f'%{name}%')).all()
            obj_all += query

        obj_id = [obj.id for obj in obj_all]
        return obj_id
