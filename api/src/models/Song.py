from .AudioFile import AudioFile
from api import db

class Song(AudioFile):
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity':'song'
    }

    def __repr__(self):
        return f"name: {self.name}, Audio type: {self.audio_type}, Uploaded:{self.uploaded_time}"
