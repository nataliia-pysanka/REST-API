from mock_alchemy.mocking import AlchemyMagicMock
from app.crud.movie import CRUDMovie
from app.crud.base import CRUDAbstract
from app.domain.base import DomainBase
from app.domain.director import DomainDirector



class FakeRepository(CRUDAbstract):
    storage = {}
    index = 0

    def create(self, session, obj_data):
        self.index += 1
        obj = {self.index: obj_data}
        self.storage.update(obj)

        session.commit()
        return self.index, obj_data

    def read(self, session, id):
        if id in self.storage:
            return id, self.storage[id]

    def read_all(self, session, offset: int = 0, limit: int = 10):
        lst = []
        for item in range(1 + offset, 1 + offset + limit + 1):
            if self.storage.get(item):
                lst.append((item, self.storage[item]))
            else:
                break
        return lst

    def update(self, session, obj, update_obj):
        index, data = obj
        try:
            for key, value in update_obj.items():
                if key in data:
                    data[key] = value
            self.storage[index] = data
        except AttributeError:
            return None
        return index, data

    def delete(self, session, id):
        obj = self.storage.get(id, None)
        if obj:
            del self.storage[id]
        return id, obj


def test_domain_base(flask_app_mock):
    repo, session = FakeRepository(), AlchemyMagicMock()
    domain = DomainBase(repo)
    with flask_app_mock.app_context():
        resp0 = domain.read_all(session)
        resp1 = domain.create(session, {"Nickname": "admin"})
        resp2 = domain.read(session, 1)
        resp3 = domain.read_all(session)
        resp4 = domain.update(session, (1, {"Nickname": "admin"}),
                              {"Nickname": "user"})
        resp5 = domain.update(session, (1, {"Nickname": "admin"}), 88)
        resp6 = domain.create(session, {"some data": "data"})
        resp7 = domain.read_all(session)
        resp8 = domain.delete(session, 1)
        resp9 = domain.read(session, 1)
        resp10 = domain.read(session, 2)
    assert resp0 == []
    assert resp1 == (1, {"Nickname": "admin"})
    assert resp2 == (1, {"Nickname": "admin"})
    assert resp3 == [(1, {"Nickname": "admin"})]
    assert resp4 == (1, {"Nickname": "user"})
    assert resp5 is None
    assert resp6 == (2, {"some data": "data"})
    assert resp7 == [(1, {"Nickname": "user"}), (2, {"some data": "data"})]
    assert resp8 == (1, {"Nickname": "user"})
    assert resp9 is None
    assert resp10 == (2, {"some data": "data"})
