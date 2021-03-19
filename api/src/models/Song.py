from .AudioFile import AudioFile
from api import db, ma
from marshmallow import fields, validate, validates
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class Song(AudioFile):
    __tablename__ = 'song'
    
    id = db.Column(db.Integer, db.ForeignKey('audiofile.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'song'
    }

    def __repr__(self):
        return f"name: {self.name}, Audio type: {self.audio_type}, Uploaded:{self.uploaded_time}"

class SongSchema(SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id', 'name', 'duration', "uploaded_time")
        model = Song
        load_instance = True
    
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    duration = fields.Integer(required=True, validate=validate.Range(min=0))
    uploaded_time = fields.DateTime(dump_only=True)