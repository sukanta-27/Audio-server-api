from .AudioFile import AudioFile
from .Person import Person
from .Host import Host, HostSchema
from .Participant import Participant, ParticipantSchema
from api import db, ma
from marshmallow import fields, validates, validate

participantList = db.Table(
    'participantList',
    db.Column('participant_id', db.Integer, db.ForeignKey('participant.id'), primary_key=True),
    db.Column('podcast_id', db.Integer, db.ForeignKey('podcast.id'), primary_key=True),
    extend_existing=True 
)

class Podcast(AudioFile):
    __tablename__ = 'podcast'

    id = db.Column(db.Integer, db.ForeignKey('audiofile.id'), primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'), nullable=False)
    host = db.relationship(
        'Host',
        backref="podcasts"
    )
    
    participants = db.relationship(
        'Participant',
        secondary=participantList,
        lazy='subquery',
        backref=db.backref('podcasts', lazy=True)
    )

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
