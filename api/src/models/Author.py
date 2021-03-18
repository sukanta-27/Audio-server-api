from api import db, ma
from .Person import Person
from marshmallow import fields, validate

class Author(Person):
    __tablename__ = "author"
    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)

    __mapper_args__= {
        'polymorphic_identity': 'author'
    }

    def __repr__(self):
        return f"Author: {self.name}"