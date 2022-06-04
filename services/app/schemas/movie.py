from marshmallow_sqlalchemy import auto_field
from app.ma import ma
from app.models.movie import MovieModel
from app.schemas.director import DirectorSchema
from app.schemas.poster import PosterSchema
from app.schemas.user import UserSchema


class MovieSchema(ma.SQLAlchemyAutoSchema):
    id = auto_field()

    directors = ma.Nested(DirectorSchema, many=True, nullable=True)
    posters = ma.Nested(PosterSchema, many=True, nullable=True)
    user = ma.Nested(UserSchema)

    class Meta:
        model = MovieModel
        dateformat = '%Y-%m-%d'
        load_instance = True
        include_fk = True
        include_relationships = True
