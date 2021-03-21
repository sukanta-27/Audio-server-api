from .AudioFile import AudioFile
from api import db, ma
from marshmallow import fields, validate, validates
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class Song(AudioFile):
    """
    Inherits from AudioFile class.

    The relationship between theparent class and subclasses 
    follow the "Joined Table Inheritance" (https://docs.sqlalchemy.org/en/13/orm/inheritance.html)

    fields:
        id: Integer,
        name: String [max length = 100],
        duratioin: Integer [Positive only],
        audio_type: Field used for the polymorphic_on property for sqlalchemy model

    methods:
        classmethod: find_by_id: Return an instance from database based on id
        classmethod: find_by_name: Retrun an instance from database based on name (first occurrance)
        instancemethod: save_to_db(self) -> saves record to database
        instancemethod: delete_from_db(self) -> Deletes record from database
        
        staticmethod: update(data, record): Updates the record with the data and commits to database

    """
    __tablename__ = 'song'
    
    id = db.Column(db.Integer, db.ForeignKey('audiofile.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'song'
    }

    @staticmethod
    def update(data, record):
        if "name" in data:
            record.name = data["name"]
        if "duration" in data:
            record.duration = data["duration"]
        
        db.session.commit()
        return record

    def __repr__(self):
        return f"name: {self.name}, Audio type: {self.audio_type}, Uploaded:{self.uploaded_time}"

class SongSchema(SQLAlchemyAutoSchema):
    """
    The SongSchema class Inherits from the marshmallow_sqlalchemy SQLAlchemyAutoSchema class.

    It is used to validate the request data and serialise/deserialise the Song class instance.

    Fields shown when dumped as json:
        ('id','name', 'duration', 'uploaded_time')
    
    Fields needed to load an instance:
        required = 'name', 'duration'
    """
    class Meta:
        ordered = True
        fields = ('id', 'name', 'duration', "uploaded_time")
        model = Song
        load_instance = True
    
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    duration = fields.Integer(required=True, validate=validate.Range(min=0))
    uploaded_time = fields.DateTime(dump_only=True)