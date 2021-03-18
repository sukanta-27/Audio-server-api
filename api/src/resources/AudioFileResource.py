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
    
    def isValidInput(self, audioFileType, audioFileID):
        if self.isValidAudioFileType(audioFileType) and audioFileID.isnumeric():
            return True

        return False

    def get(self, audioFileType, audioFileID):
        if self.isValidInput(audioFileType, audioFileID):
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
        if self.isValidInput(audioFileType, audioFileID):
            pass

        return {'Message': 'AudioFileType or AudioFileID is not valid'}, 400
    
    def delete(self, audioFileType, audioFileID):
        if self.isValidInput(audioFileType, audioFileID):
            audioFileID = int(audioFileID)
            responseData = {}
            status_code = 400

            if audioFileType == 'song':
                song = Song.query.filter_by(id=audioFileID).first()
                if song:
                    db.session.delete(song)
                    db.session.commit()
                    responseData['Message'] = 'Successfully deleted record'
                    status_code = 200
                else:
                    responseData['Message'] = f"No Song with id:{audioFileID} found"

            elif audioFileType == 'podcast':
                podcast = Podcast.query.filter_by(id=audioFileID).first()
                if podcast:
                    db.session.delete(podcast)
                    db.session.commit()
                    responseData['Message'] = 'Successfully deleted record'
                    status_code = 200
                else:
                    responseData['Message'] = f"No Podcast with id:{audioFileID} found"

            elif audioFileType == 'audiobook':
                audiobook = AudioBook.query.filter_by(id=audioFileID).first()
                if audiobook:
                    db.session.delete(audiobook)
                    db.session.commit()
                    responseData['Message'] = 'Successfully deleted record'
                    status_code = 200
                else:
                    responseData['Message'] = f"No Audiobook with id:{audioFileID} found"

            return responseData, status_code
               
        return {'Message': 'AudioFileType or AudioFileID is not valid'}, 400