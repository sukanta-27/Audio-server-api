from api import db, ma
from .Person import Person
from marshmallow import fields, validate

class Host(Person):
    __tablename__ = "host"
    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)

    __mapper_args__= {
        'polymorphic_identity': 'host'
    }

    def __repr__(self):
        return f"Host: {self.name}"

class HostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Host
        load_instance = True

    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))