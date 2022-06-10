from app.domain.base import DomainBase
from typing import Dict, Any, List

from app.db import db


class DomainGenre(DomainBase):
    def get_id_by_name(self, name_list: List[str]) -> List[Any]:
        if name_list:
            return self.crud.get_id_by_name(db.session, name_list)
        return []
