import logging
from api.src.models.Song import Song, SongSchema
from api.src.models.AudioBook import AudioBook, AudioBookSchema
from api.src.models.Podcast import Podcast, PodcastSchema
from flask_restful import Resource
from api import db

class AudioListResource(Resource):

    def isValidAudioFileType(self, audioFileType):
        if audioFileType not in ['song', 'podcast', 'audiobook']:
            return False
        return True

    def get(self, audioFileType):
        if self.isValidAudioFileType(audioFileType):

            if audioFileType == 'song':
                schema = SongSchema()
                songs = Song.query.all()
                data = schema.dump(songs, many=True)

                return data, 200

            elif audioFileType == 'podcast':
                schema = PodcastSchema()
                podcasts = Podcast.query.all()
                data = schema.dump(podcasts, many=True)

                return data, 200

            elif audioFileType == 'audiobook':
                schema = AudioBookSchema()
                audiobooks = AudioBook.query.all()
                data = schema.dump(audiobooks, many=True)

                return data, 200

        logging.warn(f"{audioFileType} is not a supported file type")
        return {'Message': f"{audioFileType} is not a supported file type"}, 400