from sqlalchemy.orm import Session
from app.schemas.movie import MovieSchema
from app.CRUD.base import CRUDBase
from app.models.movie import MovieModel
from typing import Any, List


class CRUDMovie(CRUDBase[MovieModel, MovieSchema]):
    def create(self, session: Session, obj_data: Any) -> MovieModel:
        db_obj = self.model(title=obj_data.title,
                            description=obj_data.description,
                            date_release=obj_data.date_release,
                            rating=obj_data.rating,
                            id_director=obj_data.id_director,
                            id_poster=obj_data.id_poster,
                            id_user=obj_data.id_user)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj
