from .AudioFile import AudioFile
from api import db

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
