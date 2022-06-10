from app.crud.genre import CRUDGenre
from app.crud.director import CRUDDirector

from app.domain.base import DomainBase

from app.db import db


class DomainUser(DomainBase):
    def get_user_by_nickname(self, nickname: str):
        return self.crud.get_user_by_nickname(db.session, nickname)
