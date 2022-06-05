from sqlalchemy.orm import Session
from app.schemas.poster import PosterSchema
from app.CRUD.base import CRUDBase
from app.models.poster import PosterModel
from typing import Any, List


class CRUDPoster(CRUDBase[PosterModel, PosterSchema]):
    def create(self, session: Session, obj_data: Any) -> PosterModel:
        db_obj = self.model(url=obj_data.url)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

