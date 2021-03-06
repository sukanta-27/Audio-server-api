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
    """
    Inherits from AudioFile class.

    The relationship between theparent class and subclasses 
    follow the "Joined Table Inheritance" (https://docs.sqlalchemy.org/en/13/orm/inheritance.html)

    fields:
        id: Integer,
        name: String [max length = 100],
        duratioin: Integer [Positive only],
        audio_type: Field used for the polymorphic_on property for sqlalchemy model
        host: can be passed as a string or a Host(Parent:Person) class
        Participants: Holds a Many-to-many relationship with the Podcast class
    methods:
        classmethod: find_by_id: Return an instance from database based on id
        classmethod: find_by_name: Retrun an instance from database based on name (first occurrance)
        instancemethod: save_to_db(self) -> saves record to database
        instancemethod: delete_from_db(self) -> Deletes record from database
        
        staticmethod: update(data, record): Updates the record with the data and commits to database

    """
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

        if not all([
            isinstance(name, str), 
            isinstance(duration, int), 
            isinstance(host, (str, Host))
        ]):
            raise TypeError("A required field does not have the correct type")

        if len(participants) > 10:
            raise ValidationError("Podcast cannot have more than 10 participants")

        AudioFile.__init__(self, name, duration)
        self.host = host if isinstance(host, Host) else Host(host)
        if all(isinstance(i, Participant) for i in participants):
            self.participants.extend(participants)
        else:
            participants = [Participant(i) for i in participants]
            self.participants.extend(participants)

    @staticmethod
    def update(data, record):
        if "name" in data:
            record.name = data["name"]
        if "duration" in data:
            record.duration = data["duration"]
        if "host" in data:
            record.host = data["host"]
        if "participants" in data:
            record.participants = data["participants"]
        
        db.session.commit()
        return record

    def __repr__(self):
        return f"name: {self.name}, Audio type: {self.audio_type}" +\
            f", Host:{self.host}, participants: {self.participants}"

class PodcastSchema(SQLAlchemyAutoSchema):
    """
    The PodcastSchema class Inherits from the marshmallow_sqlalchemy SQLAlchemyAutoSchema class.

    It is used to validate the request data and serialise/deserialise the Podcast class instance

    Fields shown when dumped as json:
        ('id','name', 'duration', 'host', 'participants', 'uploaded_time')
    
    Fields needed to load an instance:
        required = 'name', 'duration', 'host'
        optional = 'participants'

    host, participants fields are not nested fields, they are passed to the class as input and gets converted
    to the correct class instance using the @post_load method. This is done to make the system a little flexible
    for the end user.
    """    
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

    @post_load(pass_original=True)
    def make_instance(self, data, id, **kwargs):
        # Check if record already exists
        record = None
        if "id" in id:
            record = Podcast.find_by_id(id["id"])

        # Make Participants field optional
        if "participants" not in data:
            data["participants"] = [] if not record else record.participants
        else:        
            # Add limit of 10 participants
            if len(data["participants"]) > 10:
                raise ValidationError("Podcast can not have more than 10 participants")

            # Arrange participants in correct format and create Participant object list
            participantList = [{"name": i} for i in data["participants"]]
            data["participants"] = [ParticipantSchema().load(i, session=db.session) for i in participantList]

        if "host" in data:    
            data["host"] = HostSchema().load({"name": data["host"]}, session=db.session)
        
        return Podcast(**data) if not record else Podcast.update(data, record)
