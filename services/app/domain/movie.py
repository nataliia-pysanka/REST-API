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
        offset = int(args.get('offset', '0'))
        limit = int(args.get('limit', '10'))

        if args.get('genre') is None and \
                args.get('release_date') is None and \
                args.get('director') is None:
            return self.crud.read_all(db.session, offset=offset, limit=limit)

        genres = args.get('genre', '')
        release_dates = args.get('release_date', '')
        directors = args.get('director', '')
        genres = genres.split(' ')
        release_dates = [datetime.strptime(item, '%Y-%m-%d')
                         for item in release_dates.split(',') if item]

        directors = directors.split(' ')

        id_genre = genre_domain.get_id_by_name(genres)
        id_director = director_domain.get_id_by_name(directors)

        return self.crud.get_by_filter(db.session,
                                       id_genre=id_genre,
                                       release_date=release_dates,
                                       id_director=id_director,
                                       offset=offset,
                                       limit=limit)

    def get_id_by_filter(self, **kwargs):
        return self.crud.get_id_by_filter(db.session, kwargs)
