from app.crud.base import CRUDAbstract
from sqlalchemy.orm import Session
from typing import Dict, Any


class DomainBase:
    def __init__(self, crud: CRUDAbstract):
        self.crud = crud

    def create(self, session: Session, obj_data: Any):
        return self.crud.create(session, obj_data)

    def read(self, session: Session, id: Any):
        return self.crud.read(session, id)

    def read_all(self, session: Session):
        return self.crud.read_all(session)

    def update(self, session: Session, obj_data: Any, id: Any):
        return self.crud.update(session, obj_data, id)

    def delete(self, session: Session, id: Any):
        return self.crud.delete(session, id)
