from api import db, ma
from .Person import Person
from marshmallow import fields, validate

class Narrator(Person):
    __tablename__ = None

    audiobook_id = db.Column(db.Integer, db.ForeignKey('audiobook.id'), nullable=False)
    
    __mapper_args__= {
        'polymorphic_identity': 'narrator'
    }

    def __repr__(self):
        return f"Narrator: {self.name}"