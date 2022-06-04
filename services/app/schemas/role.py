from marshmallow_sqlalchemy import auto_field
from app.ma import ma
from app.models.role import RoleModel


class RoleSchema(ma.SQLAlchemyAutoSchema):
    id = auto_field()

    class Meta:
        model = RoleModel
        load_instance = True
        load_only = ("user",)
        include_fk = True
        include_relationships = True
