from .AudioFile import AudioFile
from .Person import Person
from .Host import Host, HostSchema
from .Participant import Participant, ParticipantSchema
from api import db, ma
from marshmallow import fields, validate, post_load, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

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

    def __init__(self, name, duration, host, participants=[], **kwargs):
        AudioFile.__init__(self, name, duration)
        self.host = host
        self.participants.extend(participants)

    def __repr__(self):
        return f"name: {self.name}, Audio type: {self.audio_type}, Host:{self.host}"

class PodcastSchema(SQLAlchemyAutoSchema):
    class Meta:
        ordered = True
        fields = ("id", "name", "duration", "host", "participants", "uploaded_time")
        model = Podcast
        load_instance = True
    
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    duration = fields.Integer(required=True, validate=validate.Range(min=0))
    host = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    participants = fields.List(fields.Str(validate=validate.Length(min=1, max=100)))
    uploaded_time = fields.DateTime(dump_only=True)

    @post_load
    def make_instance(self, data, **kwargs):
        # Make Participants field optional
        if "participants" not in data:
            data["participants"] = []
        
        # Add limit of 10 participants
        if len(data["participants"]) > 10:
            raise ValidationError("Podcast can not have more than 10 participants")

        # Arrange participants in correct format and create Participant object list
        participantList = [{"name": i} for i in data["participants"]]
        data["participants"] = [ParticipantSchema().load(i, session=db.session) for i in participantList]
        data["host"] = HostSchema().load({"name": data["host"]}, session=db.session)
        return Podcast(**data)
