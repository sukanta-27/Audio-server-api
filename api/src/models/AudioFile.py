from api import db
from datetime import datetime

class AudioFile(db.Model):
    __tablename__ = 'audiofile'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # TODO: Duration can not be negative, add constraint
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
