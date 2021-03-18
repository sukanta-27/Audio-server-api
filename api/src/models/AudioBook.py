from .AudioFile import AudioFile
from api import db, ma
from api.src.models.Person import Person
from api.src.models.Author import Author
from api.src.models.Narrator import Narrator
from marshmallow import fields, validate, validates

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
        return f"name: {self.name}, Audio type: {self.audio_type}, \
            Author: {self.author}, narrator: {self.narrator}"

class AudioBookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AudioBook
        load_instance = True
    
    id = fields.Integer(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    duration = fields.Integer(required=True, validate=validate.Range(min=0))
    author = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    narrator = fields.Str(required=True, validate=validate.Length(min=1, max=100))
