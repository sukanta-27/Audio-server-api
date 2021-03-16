from .AudioFile import AudioFile
from api import db, ma
from marshmallow import fields, validate, validates

class AudioBook(AudioFile):
    __tablename__ = None

    author = db.Column(db.String(100))
    narrator = db.Column(db.String(100))

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
