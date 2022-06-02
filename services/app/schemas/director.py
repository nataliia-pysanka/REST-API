from marshmallow_sqlalchemy import auto_field
from app.ma import ma
from app.models.director import DirectorModel
from app.models.movie import MovieModel


class DirectorSchema(ma.SQLAlchemyAutoSchema):
    id = auto_field()

    class Meta:
        model = DirectorModel
        dateformat = '%Y-%m-%d'
        load_instance = True
        load_only = ("movie",)
        include_fk = True
        include_relationships = True
