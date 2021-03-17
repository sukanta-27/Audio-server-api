from api.src.models.AudioFile import AudioFile
from api.src.models.Song import Song, SongSchema
from api.src.models.AudioBook import AudioBook, AudioBookSchema
from api.src.models.Podcast import Podcast, PodcastSchema
from flask_restful import Resource
from api import db

class AudioFileResource(Resource):

    def isValidAudioFileType(self, audioFileType):
        if audioFileType not in ['song', 'podcast', 'audiobook']:
            return False
        return True
    
    def get(self, audioFileType, audioFileID):
        if self.isValidAudioFileType(audioFileType) and audioFileID.isnumeric():
            responseData = None
            audioFileID = int(audioFileID)
            
            if audioFileType == 'song':
                schema = SongSchema()
                song = Song.query.filter_by(id=audioFileID).first()

                if song:
                    responseData = schema.dump(song)

            elif audioFileType == 'podcast':
                schema = PodcastSchema()
                podcast = Podcast.query.filter_by(id=audioFileID).first()

                if podcast:
                    responseData = schema.dump(podcast)

            elif audioFileType == 'audiobook':
                schema = AudioBookSchema()
                audiobook = AudioBook.query.filter_by(id=audioFileID).first()

                if audiobook:
                    responseData = schema.dump(audiobook)
            
            if responseData:
                return responseData, 200
            
            return {'Message': 'File not found'}, 400

        return {'Message': 'AudioFileType or AudioFileID is not valid'}, 400 

    def put(self, audioFileType, audioFileID):
        if self.isValidAudioFileType(audioFileType) and isinstance(audioFileID, int):
            pass

        return {'Message': 'AudioFileType or AudioFileID is not valid'}, 400
    
    def delete(self, audioFileType, audioFileID):
        if self.isValidAudioFileType(audioFileType) and isinstance(audioFileID, int):
            pass

        return {'Message': 'AudioFileType or AudioFileID is not valid'}, 400