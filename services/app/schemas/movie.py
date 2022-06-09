from marshmallow_sqlalchemy import auto_field
from app.ma import ma
from app.models.movie import MovieModel
from app.schemas.director import DirectorSchema
from app.schemas.poster import PosterSchema
from app.schemas.user import UserSchema
from app.schemas.genre import GenreSchema


class MovieSchema(ma.SQLAlchemyAutoSchema):
    id = auto_field()

    genre = ma.Nested(GenreSchema)
    director = ma.Nested(DirectorSchema)
    poster = ma.Nested(PosterSchema)
    user = ma.Nested(UserSchema)

    class Meta:
        model = MovieModel

        exclude = ('id', 'id_genre', 'id_director', 'id_poster', 'id_user')
        dateformat = '%Y-%m-%d'
        load_instance = True
        include_fk = True
        include_relationships = True
        ordered = True
