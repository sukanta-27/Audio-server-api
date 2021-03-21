from api import db
from datetime import datetime

class AudioFile(db.Model):
    """
    AudioFile class is a SQLAlchemy model that is used as a base class 
    for all the supported audio types: song, podcast, audiobook.

    The relationship between the subclasses follow the "Joined Table Inheritance" (https://docs.sqlalchemy.org/en/13/orm/inheritance.html)

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
    """
    __tablename__ = 'audiofile'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    audio_type = db.Column(db.String(10), nullable=False)
    uploaded_time = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    __mapper_args__ = {
        'polymorphic_on':audio_type,
        'polymorphic_identity':'audiofile'
    }

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
