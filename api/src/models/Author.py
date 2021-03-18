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

class AuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Author
        load_instance = True

    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))