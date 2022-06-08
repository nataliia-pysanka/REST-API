from sqlalchemy.orm import Session
from app.schemas.genre import GenreSchema
from app.CRUD.base import CRUDBase
from app.models.genre import GenreModel
from typing import Any, List


class CRUDGenre(CRUDBase[GenreModel, GenreSchema]):
    def create(self, session: Session, obj_data: Any) -> GenreModel:
        db_obj = self.model(name=obj_data.name)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def get_id_by_name(self, session: Session, name_list: List[str]) -> Any:
        obj_id = []
        for name in name_list:
            obj_all = session.query(self.model).filter(self.model.name.ilike(
                f'%{name}%')).all()
            for obj in obj_all:
                obj_id.append(obj.id)
        return obj_id
