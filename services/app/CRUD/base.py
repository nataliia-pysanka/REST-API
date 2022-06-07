from sqlalchemy.orm import Session
from typing import List, Generic, TypeVar, Type, Any, Dict
from flask.json import JSONEncoder
BaseModel = TypeVar("BaseModel")
BaseSchema = TypeVar("BaseSchema")


class CRUDBase(Generic[BaseModel, BaseSchema]):
    def __init__(self, model: Type[BaseModel]):
        self.model = model

    def create(self, session: Session, obj_data: Dict) -> BaseModel:
        db_obj = self.model(**obj_data)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def read(self, session: Session, id: Any) -> BaseModel:
        return session.query(self.model).get(id)

    def read_all(self, session: Session, skip: int = 0, limit: int = 100) \
            -> List[BaseModel]:
        return session.query(self.model).offset(skip).limit(limit).all()

    def update(self, session: Session, obj_data: Any, id: Any) -> BaseModel:
        db_obj = session.query(self.model).get(id)
        if db_obj:
            for field in obj_data:
                setattr(db_obj, field, obj_data[field])

            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return db_obj

    def delete(self, session: Session, id: Any) -> BaseModel:
        db_obj = session.query(self.model).get(id)
        if db_obj:
            session.delete(db_obj)
            session.commit()
            return db_obj

    def get_id_by_name(self, session: Session, name: str) -> Any:
        obj = session.query(self.model).filter(self.model.name.ilike(
            f'%{name}%')).first()
        if obj:
            return obj.id
        return None

