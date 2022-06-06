from sqlalchemy.orm import Session

from sqlalchemy import or_
from app.schemas.movie import MovieSchema
from app.CRUD.base import CRUDBase
from app.models.movie import MovieModel
from typing import Any, List, Dict


class CRUDMovie(CRUDBase[MovieModel, MovieSchema]):
    def create(self, session: Session, obj_data: Any) -> MovieModel:
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

    def get_by_filter(self, session: Session, id_genre: Any = None,
                      release: List[str] = [], id_director: Any = None,
                      skip: int = 0, limit: int = 100) -> List[MovieModel]:
        return session.query(self.model).filter(or_(
                    self.model.id_genre == id_genre,
                    # self.model.date_release > release[0],
                    # self.model.date_release < release[1],
                    self.model.id_director == id_director
                                      )).offset(skip).limit(limit).all()

