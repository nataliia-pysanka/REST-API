from marshmallow_sqlalchemy import auto_field
from app.ma import ma
from app.models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    id = auto_field()

    class Meta:
        model = UserModel
        dateformat = '%Y-%m-%d'
        load_instance = True
        load_only = ("movies",)
        include_fk = True
        include_relationships = True
