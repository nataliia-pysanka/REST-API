from app.crud.base import CRUDAbstract
from typing import Dict, Any

from app.db import db


class DomainBase:
    def __init__(self, crud: CRUDAbstract):
        self.crud = crud

    def create(self, obj_data: Dict):
        print(type(obj_data))
        return self.crud.create(db.session, obj_data)

    def read(self, id: Any):
        return self.crud.read(db.session, id)

    def read_all(self):
        return self.crud.read_all(db.session)

    def update(self, obj_data: Any, id: Any):
        return self.crud.update(db.session, obj_data, id)

    def delete(self, id: Any):
        return self.crud.delete(db.session, id)
