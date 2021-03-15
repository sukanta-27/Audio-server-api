from .AudioFile import AudioFile
from api import db

class AudioBook(AudioFile):
    __tablename__ = None

    author = db.Column(db.String(100))
    narrator = db.Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_identity':'audiobook'
    }

    def __init__(self, name, duration, author, narrator, **kwargs):
        AudioFile.__init__(self, name, duration)
        self.author = author
        self.narrator = narrator

    def __repr__(self):
        return f"name: {self.name}, Audio type: {self.audio_type}, \
            Author: {self.author}, narrator: {self.narrator}"
