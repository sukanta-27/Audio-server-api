from .AudioFile import AudioFile
from api import db, ma
from api.src.models.Person import Person
from api.src.models.Author import Author, AuthorSchema
from api.src.models.Narrator import Narrator, NarratorSchema
from marshmallow import fields, validate, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class AudioBook(AudioFile):
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
        AudioFile.__init__(self, name, duration)
        self.author = author
        self.narrator = narrator

    def __repr__(self):
        return f"name: {self.name}, Audio type: {self.audio_type}, Author: {self.author}, narrator: {self.narrator}"

class AudioBookSchema(SQLAlchemyAutoSchema):
    class Meta:
        ordered = True
        fields = ('id','name', 'duration', 'author', 'narrator', 'uploaded_time')
        model = AudioBook
        load_instance = True
    
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    duration = fields.Integer(required=True, validate=validate.Range(min=0))
    # author = fields.Nested(AuthorSchema(only=('name',)))
    # narrator = fields.Nested(NarratorSchema(only=('name',)))

    # Add Str field instead of Nested to support only passing string instead of JSON
    author = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    narrator = fields.Str(required=True, validate=validate.Length(min=1, max=100))

    @post_load
    def make_instance(self, data, **kwargs):
        data['author'] = AuthorSchema().load({"name": data["author"]}, session=db.session)
        data['narrator'] = NarratorSchema().load({"name": data["narrator"]}, session=db.session)
        return AudioBook(**data)