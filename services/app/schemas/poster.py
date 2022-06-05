from marshmallow_sqlalchemy import auto_field
from app.ma import ma
from app.models.poster import PosterModel


class PosterSchema(ma.SQLAlchemyAutoSchema):
    id = auto_field()

    class Meta:
        model = PosterModel
        exclude = ('id',)
        load_instance = True
        load_only = ("movie",)
        include_fk = True
        include_relationships = True
        ordered = True
