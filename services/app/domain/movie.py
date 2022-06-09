from datetime import datetime
from app.crud.genre import CRUDGenre
from app.crud.director import CRUDDirector

from app.domain.base import DomainBase
from app.domain.director import DomainDirector
from app.domain.genre import DomainGenre

from app.db import db

genre_domain = DomainGenre(CRUDGenre())
director_domain = DomainDirector(CRUDDirector())


class DomainMovie(DomainBase):
    def get_movie_by_filter(self, args):
        genres = args.get('genre', '').split(' ')
        release_dates = [datetime.strptime(item, '%Y-%m-%d')
                         for item in args.get('release_date', '').split(',')
                         if item]

        directors = args.get('director', '').split(' ')

        id_genre = genre_domain.get_id_by_name(genres)
        id_director = director_domain.get_id_by_name(directors)

        offset = int(args.get('offset'), 0)
        limit = int(args.get('limit'), 10)

        return self.crud.get_by_filter(db.session,
                                       id_genre=id_genre,
                                       release_date=release_dates,
                                       id_director=id_director,
                                       offset=offset,
                                       limit=limit)

    def get_id_by_filter(self, **kwargs):
        return self.crud.get_id_by_filter(db.session, kwargs)
