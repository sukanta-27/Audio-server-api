from api import db, ma
from .Person import Person
from marshmallow import fields, validate

class Narrator(Person):
    __tablename__ = "narrator"
    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)

    __mapper_args__= {
        'polymorphic_identity': 'narrator'
    }

    def __repr__(self):
        return f"Narrator: {self.name}"