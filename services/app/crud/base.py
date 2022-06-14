"""Module for base class with CRUD operations"""
from typing import List, Generic, TypeVar, Type, Any, Dict, Optional, Union
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from app.util.log import logger

@as_declarative()
class Base:
    """Class decorator which will adapt a given class into a
    declarative_base()."""
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
        """Creates operation"""
        pass

    @abstractmethod
    def read(self, session: Session, id: Any):
        """Reads operation"""
        pass

    @abstractmethod
    def read_all(self, session: Session, offset: int = 0, limit: int = 10):
        """Reads all operation"""
        pass

    @abstractmethod
    def update(self, session: Session, obj: ModelType, update_obj: Any):
        """Updates operation"""
        pass

    @abstractmethod
    def delete(self, session: Session, id: Any):
        """Deletes operation"""
        pass


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType],
               CRUDAbstract):
    """Class-generic for base CRUD operations"""
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, session: Session, obj: CreateSchemaType) -> ModelType:
        """Creates object and save to session"""
        db_obj = self.model(obj)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def read(self, session: Session, id: Any) -> ModelType:
        """Reads object by id"""
        return session.query(self.model).get(id)

    def read_all(self, session: Session, offset: int = 0, limit: int = 10) \
            -> Optional[List[ModelType]]:
        """Reads all objects"""
        return session.query(self.model).offset(offset).limit(limit).all()

    def update(self, session: Session, obj: ModelType,
               update_obj: Union[UpdateSchemaType, Dict[str, any]]) \
            -> Optional[ModelType]:
        """Updates object by id and save session"""
        if isinstance(update_obj, dict):
            update_data = update_obj
        else:
            update_data = update_obj.dict()

        try:
            for field in update_data:
                setattr(obj, field, update_data[field])
        except AttributeError as err:
            logger.error(err)
            return None

        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def delete(self, session: Session, id: Any) -> Optional[ModelType]:
        """Deletes object by id and save session"""
        db_obj = session.query(self.model).get(id)
        if db_obj:
            session.delete(db_obj)
            session.commit()
            return db_obj

    def get_id_by_filter(self, session: Session, kwargs) \
            -> Optional[List[ModelType]]:
        """Returns id of object by filter"""
        obj_all = session.query(self.model).filter_by(**kwargs).all()
        obj_id = [obj.id for obj in obj_all]
        return obj_id
