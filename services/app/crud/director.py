from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.schemas.director import DirectorSchema
from app.crud.base import CRUDBase
from app.models.director import DirectorModel
from typing import Any, List


class CRUDDirector(CRUDBase[DirectorModel, DirectorSchema]):
    def __init__(self):
        self.model = DirectorModel

    def create(self, session: Session, obj_data: Any) -> DirectorModel:
        db_obj = self.model(name=obj_data.name,
                            surname=obj_data.surname,
                            date_birth=obj_data.date_birth,
                            wiki_url=obj_data.wiki_url)

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def get_id_by_name(self, session: Session, name_list: List[str]) -> Any:
        if len(name_list) == 2:
            obj_all = session.query(self.model).filter(
                                self.model.name.ilike(name_list[0]),
                                self.model.surname.ilike(name_list[1])).all()
        elif len(name_list) == 1:
            obj_all = session.query(self.model).filter(or_(
                            self.model.name.ilike(name_list[0]),
                            self.model.surname.ilike(name_list[0]))).all()
        obj_id = [obj.id for obj in obj_all]
        return obj_id

    def get_birth_by_id(self, session: Session, id: Any) -> Any:
        obj = session.query(self.model).filter(self.model.id == id).first()
        if obj:
            return obj.date_birth
        return None