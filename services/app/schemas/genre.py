from marshmallow_sqlalchemy import auto_field
from app.ma import ma
from app.models.genre import GenreModel


class GenreSchema(ma.SQLAlchemyAutoSchema):
    id = auto_field()

    class Meta:
        model = GenreModel
        exclude = ('id',)
        load_instance = True
        load_only = ("movie",)
        include_fk = True
        include_relationships = True
        ordered = True
