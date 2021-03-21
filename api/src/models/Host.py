from api import db, ma
from .Person import Person
from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class Host(Person):
    """
    Host inherits from the Person base class

    The relationship between the subclasses follow the "Joined Table Inheritance" (https://docs.sqlalchemy.org/en/13/orm/inheritance.html)

    It holds a One-to-many relationship with the Podcast class

    fields:
        id: Integer,
        name: String [max length = 100]
    """    
    __tablename__ = "host"
    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)

    __mapper_args__= {
        'polymorphic_identity': 'host'
    }

    def __repr__(self):
        return f"{self.name}"

class HostSchema(SQLAlchemyAutoSchema):
    class Meta:
        fields = ("name",)
        model = Host
        load_instance = True

    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))