from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from typing import List, Generic, TypeVar, Type, Any, Dict, Optional, Union


@as_declarative()
class Base:
    id: Any
    __name__: str
    
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=ModelType)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=ModelType)


class CRUDAbstract(ABC):
    @abstractmethod
    def create(self, session: Session, obj_data: Dict):
        pass

    @abstractmethod
    def read(self, session: Session, id: Any):
        pass

    @abstractmethod
    def read_all(self, session: Session, offset: int = 0, limit: int = 10):
        pass

    @abstractmethod
    def update(self, session: Session, obj_data: Any, id: Any):
        pass

    @abstractmethod
    def delete(self, session: Session, id: Any):
        pass


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType],
               CRUDAbstract):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, session: Session, obj: CreateSchemaType) -> ModelType:
        db_obj = self.model(obj)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def read(self, session: Session, id: Any) -> ModelType:
        return session.query(self.model).get(id)

    def read_all(self, session: Session, offset: int = 0, limit: int = 10) \
            -> Optional[List[ModelType]]:
        return session.query(self.model).offset(offset).limit(limit).all()

    def update(self, session: Session, obj: ModelType,
               update_obj: Union[UpdateSchemaType, Dict[str, any]]) \
            -> ModelType:
        if isinstance(update_obj, dict):
            update_data = update_obj
        else:
            update_data = update_obj.dict()

        for field in update_data:
            setattr(obj, field, update_data[field])

        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def delete(self, session: Session, id: Any) -> Optional[ModelType]:
        db_obj = session.query(self.model).get(id)
        if db_obj:
            session.delete(db_obj)
            session.commit()
            return db_obj

    def get_id_by_filter(self, session: Session, kwargs) \
            -> Optional[List[ModelType]]:
        obj_all = session.query(self.model).filter_by(**kwargs).all()
        obj_id = [obj.id for obj in obj_all]
        return obj_id
