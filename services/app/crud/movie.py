"""Module for sub-class CRUDMovie"""
from typing import Any, List
from sqlalchemy.orm import Session
from app.schemas.movie import MovieCreate, MovieUpdate, MovieDB
from app.crud.base import CRUDBase
from app.models.movie import Movie


class CRUDMovie(CRUDBase[Movie, MovieCreate, MovieUpdate]):
    """Class for CRUD operations with instance movie"""
    def __init__(self):
        self.model = Movie

    def create(self, session: Session, obj_data: Any) -> MovieDB:
        """Creates object and save to session"""
        db_obj = self.model(title=obj_data.title,
                            description=obj_data.description,
                            date_release=obj_data.date_release,
                            rating=obj_data.rating,
                            id_genre=obj_data.id_genre,
                            id_director=obj_data.id_director,
                            id_poster=obj_data.id_poster,
                            id_user=obj_data.id_user)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def get_by_filter(self, session: Session, id_genre: List[Any] = [],
                      release_date: List[str] = [],
                      id_director: List[Any] = [],
                      offset: int = 0, limit: int = 100) -> List[Movie]:
        """Returns object by filter"""
        return session.query(self.model).filter(
                    self.model.id_genre.in_(id_genre),
                    self.model.date_release > release_date[0],
                    self.model.date_release < release_date[1],
                    self.model.id_director.in_(id_director)
                                      ).offset(offset).limit(limit).all()
