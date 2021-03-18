from api import db, ma
from .Person import Person
from marshmallow import fields, validate

class Participant(Person):
    __tablename__ = "participant"
    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)

    __mapper_args__= {
        'polymorphic_identity': 'participant'
    }

    def __repr__(self):
        return f"Participant: {self.name}"

class ParticipantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Participant
        load_instance = True

    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))