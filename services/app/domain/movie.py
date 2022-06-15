from sqlalchemy.orm import Session
from pydantic import ValidationError
from typing import Any
from datetime import date, datetime

from app.crud.genre import CRUDGenre
from app.crud.director import CRUDDirector

from app.schemas.movie import MovieCreate, MovieUpdate, MovieDB

from app.domain.base import DomainBase
from app.domain.director import DomainDirector
from app.domain.genre import DomainGenre

from app.util.log import logger

genre_domain = DomainGenre(CRUDGenre())
director_domain = DomainDirector(CRUDDirector())


class DomainMovie(DomainBase):

    def get_movie_by_filter(self, session: Session, args):
        offset = int(args.get('offset', '0'))
        limit = int(args.get('limit', '10'))

        if args.get('genre') is None and \
                args.get('release_date') is None and \
                args.get('director') is None:
            query = self.crud.read_all(session, offset=offset, limit=limit)
            return [MovieDB.from_orm(obj).dict() for obj in query]

        genres = args.get('genre', '')
        release_dates = args.get('release_date', '')
        directors = args.get('director', '')
        genres = genres.split(' ')
        release_dates = [datetime.strptime(item, '%Y-%m-%d')
                         for item in release_dates.split(',') if item]

        directors = directors.split(' ')

        id_genre = genre_domain.get_id_by_name(genres)
        id_director = director_domain.get_id_by_name(directors)

        query = self.crud.get_by_filter(session,
                                       id_genre=id_genre,
                                       release_date=release_dates,
                                       id_director=id_director,
                                       offset=offset,
                                       limit=limit)

        if query:
            return [MovieDB.from_orm(obj).dict() for obj in query]
        return None

    def get_id_by_filter(self, session: Session, **kwargs):
        return self.crud.get_id_by_filter(session, kwargs)

    def create(self, obj_data: Any):
        try:
            data = MovieCreate.parse_obj(obj_data)
        except ValidationError as err:
            logger.error(err.raw_errors)
            return None, err

        query = super(DomainMovie, self).create(session, data)
        if query:
            return MovieDB.from_orm(query).dict(), None
        return None, None

    def read(self, session: Session, id: Any):
        query = super(DomainMovie, self).read(id)
        if query:
            return MovieDB.from_orm(query).dict()
        return None

    def read_all(self, session: Session):
        query = super(DomainMovie, self).read_all()
        lst = []
        for obj in query:
            lst.append(MovieDB.from_orm(obj).dict())
        return lst

    def delete(self, session: Session, id: Any):
        # obj = MovieDB.from_orm(self.read(id)).dict()
        query = super(DomainMovie, self).delete(session, id)
        if not query:
            return None
        return True
