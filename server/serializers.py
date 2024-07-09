from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields


from models import User,Entry,Category

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User


class EntrySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Entry


class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category