from .AudioFile import AudioFile
from api import db, ma
from api.src.models.Person import Person
from api.src.models.Author import Author, AuthorSchema
from api.src.models.Narrator import Narrator, NarratorSchema
from marshmallow import fields, validate, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class AudioBook(AudioFile):
    """
    Inherits from AudioFile class.

    The relationship between theparent class and subclasses 
    follow the "Joined Table Inheritance" (https://docs.sqlalchemy.org/en/13/orm/inheritance.html)

    fields:
        id: Integer,
        name: String [max length = 100],
        duratioin: Integer [Positive only],
        audio_type: Field used for the polymorphic_on property for sqlalchemy model
        author: can be passed as a string or a Author(Parent:Person) class
        narrator: can be passed as a string or a Narrator(Parent:Person) class
    methods:
        classmethod: find_by_id: Return an instance from database based on id
        classmethod: find_by_name: Retrun an instance from database based on name (first occurrance)
        instancemethod: save_to_db(self) -> saves record to database
        instancemethod: delete_from_db(self) -> Deletes record from database
        
        staticmethod: update(data, record): Updates the record with the data and commits to database

    """
    __tablename__ = 'audiobook'

    id = db.Column(db.Integer, db.ForeignKey('audiofile.id'), primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship(
        'Author',
        backref='audiobooks',
        foreign_keys=[author_id]
    )
    narrator_id = db.Column(db.Integer, db.ForeignKey('narrator.id'), nullable=False)
    narrator = db.relationship(
        'Narrator',
        backref='audiobooks',
        foreign_keys=[narrator_id]
    )    
    # author = db.Column(db.String(100))
    # narrator = db.Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_identity':'audiobook'
    }

    def __init__(self, name, duration, author, narrator, **kwargs):
        if not all([
            isinstance(name, str), 
            isinstance(duration, int), 
            isinstance(author, (str, Author)),
            isinstance(narrator, (str, Narrator))
        ]):
            raise TypeError("A required field does not have the correct type")

        AudioFile.__init__(self, name, duration)
        self.author = author if isinstance(author, Author) else Author(author)
        self.narrator = narrator if isinstance(narrator, Narrator) else Narrator(narrator)

    @staticmethod
    def update(data, record):
        if "name" in data:
            record.name = data["name"]
        if "duration" in data:
            record.duration = data["duration"]
        if "author" in data:
            record.author = data["author"]
        if "narrator" in data:
            record.narrator = data["narrator"]

        db.session.commit()
        return record

    def __repr__(self):
        return f"name: {self.name}, Audio type: {self.audio_type}, Author: {self.author}, narrator: {self.narrator}"

class AudioBookSchema(SQLAlchemyAutoSchema):
    """
    The AudioBookSchema class Inherits from the marshmallow_sqlalchemy SQLAlchemyAutoSchema class.

    It is used to validate the request data and serialise/deserialise the AudioBook class instance.

    Fields shown when dumped as json:
        ('id','name', 'duration', 'author', 'narrator', 'uploaded_time')
    
    Fields needed to load an instance:
        required = 'name', 'duration', 'author', 'narrator'

    author, narrator fields are not nested fields, they are passed to the class as input and gets converted
    to the correct class instance using the @post_load method. This is done to make the system a little flexible
    for the end user.
    """
    class Meta:
        ordered = True
        fields = ('id','name', 'duration', 'author', 'narrator', 'uploaded_time')
        model = AudioBook
        load_instance = True
    
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    duration = fields.Integer(required=True, validate=validate.Range(min=0))
    # author = fields.Nested(AuthorSchema(only=('name',)))
    # narrator = fields.Nested(NarratorSchema(only=('name',)))

    # Add Str field instead of Nested to support only passing string instead of JSON
    author = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    narrator = fields.Str(required=True, validate=validate.Length(min=1, max=100))

    @post_load(pass_original=True)
    def make_instance(self, data, id, **kwargs):

        # Check if record exists
        record = None
        if "id" in id:
            record = AudioBook.find_by_id(id["id"])

        if "author" in data:
            data['author'] = AuthorSchema().load({"name": data["author"]}, session=db.session)
        if "narrator" in data:
            data['narrator'] = NarratorSchema().load({"name": data["narrator"]}, session=db.session)
        
        # Update record if exists else return a new instance
        return AudioBook.update(data, record) if record else AudioBook(**data)