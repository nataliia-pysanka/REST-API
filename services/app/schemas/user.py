from marshmallow_sqlalchemy import auto_field
from app.ma import ma
from app.models.user import UserModel
from app.schemas.role import RoleSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    id = auto_field()
    role = ma.Nested(RoleSchema)

    class Meta:
        model = UserModel
        # exclude = ('id', 'id_role', )
        exclude = ('id', )
        dateformat = '%Y-%m-%d'
        load_instance = True
        include_fk = True
        include_relationships = True
        ordered = True
