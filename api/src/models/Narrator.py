from api import db, ma
from .Person import Person
from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class Narrator(Person):
    __tablename__ = "narrator"
    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)

    __mapper_args__= {
        'polymorphic_identity': 'narrator'
    }

    def __repr__(self):
        return f"{self.name}"

class NarratorSchema(SQLAlchemyAutoSchema):
    class Meta:
        fields = ('name',)
        model = Narrator
        load_instance = True

    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))