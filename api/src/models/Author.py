from api import db, ma
from .Person import Person
from marshmallow import fields, validate

class Author(Person):
    __tablename__ = None

    audiobook_id = db.Column(db.Integer, db.ForeignKey('audiobook.id'), nullable=False)
    __mapper_args__= {
        'polymorphic_identity': 'author'
    }

    def __repr__(self):
        return f"Author: {self.name}"