from .AudioFile import AudioFile
from api import db, ma
from marshmallow import fields, validates, validate

class Podcast(AudioFile):
    __tablename__ = None

    host = db.Column(db.String(100))
    # TODO: Set participant list column with max 10 participants

    __mapper_args__ = {
        'polymorphic_identity':'podcast'
    }

    def __init__(self, name, duration, host, **kwargs):
        AudioFile.__init__(self, name, duration)
        self.host = host

    def __repr__(self):
        return f"name: {self.name}, Audio type: {self.audio_type}, Host:{self.host}"

class PodcastSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "name", "duration", "host", "uploaded_time")
        model = Podcast
        load_instance = True
    
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    duration = fields.Integer(required=True, validate=validate.Range(min=0))
    host = fields.Str(required=True, validate=validate.Length(min=1, max=100))
