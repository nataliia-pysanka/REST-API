"""Module for sub-class CRUDPoster"""
from typing import Any
from sqlalchemy.orm import Session
from app.schemas.poster import PosterCreate, PosterUpdate
from app.crud.base import CRUDBase
from app.models.poster import Poster


class CRUDPoster(CRUDBase[Poster, PosterCreate, PosterUpdate]):
    """Class for CRUD operations with instance poster"""
    def __init__(self):
        self.model = Poster

    def create(self, session: Session, obj_data: Any) -> Poster:
        """Creates object and save to session"""
        db_obj = self.model(url=obj_data.url)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

