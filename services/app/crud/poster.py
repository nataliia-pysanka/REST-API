from sqlalchemy.orm import Session
from app.schemas.poster import PosterCreate, PosterUpdate
from app.crud.base import CRUDBase
from app.models.poster import Poster
from typing import Any


class CRUDPoster(CRUDBase[Poster, PosterCreate, PosterUpdate]):
    def __init__(self):
        self.model = Poster

    def create(self, session: Session, obj_data: Any) -> Poster:
        db_obj = self.model(url=obj_data.url)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

