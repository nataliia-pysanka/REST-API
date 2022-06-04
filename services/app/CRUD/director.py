from sqlalchemy.orm import Session
from app.schemas.director import DirectorSchema
from app.CRUD.base import CRUDBase
from app.models.director import DirectorModel
from typing import Any, List


class CRUDDirector(CRUDBase[DirectorModel, DirectorSchema]):
    def create(self, session: Session, obj_data: Any) -> DirectorModel:
        db_obj = self.model(name=obj_data.name,
                            surname=obj_data.surname,
                            date_birth=obj_data.date_birth,
                            wiki_url=obj_data.wiki_url)

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

