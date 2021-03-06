import logging
from api.src.models.AudioFile import AudioFile
from api.src.models.Song import Song, SongSchema
from api.src.models.AudioBook import AudioBook, AudioBookSchema
from api.src.models.Podcast import Podcast, PodcastSchema
from flask import request, jsonify
from flask_restful import Resource
from marshmallow import EXCLUDE
from api import db

class AudioFileResource(Resource):
    """
    Inherits from the flask_restful Resource class. 

    Used to handle GET/PUT/DELETE request for any type of audio file type.

    Endpoint to use: {{url}}/{{audioFileType}}/{{audioFileID}}

    Guide:
    
    - GET/DELETE a record:
         https://github.com/sukanta-27/Audio-server-api/blob/master/README.md#getdelete-a-specific-record
    - UPDATE a record: 
        https://github.com/sukanta-27/Audio-server-api/blob/master/README.md#update-a-record
    """
    def isValidAudioFileType(self, audioFileType):
        """
        Returns if audioFileType is among the supported types or not
        """
        if audioFileType not in ['song', 'podcast', 'audiobook']:
            return False
        return True
    
    def isValidInput(self, audioFileType, audioFileID):
        """
        Returns if the request data is valid or not
        """        
        if self.isValidAudioFileType(audioFileType) and audioFileID.isnumeric():
            return True

        return False

    def get(self, audioFileType, audioFileID):
        if self.isValidInput(audioFileType, audioFileID):
            responseData = None
            audioFileID = int(audioFileID)
            
            if audioFileType == 'song':
                schema = SongSchema()
                song = Song.find_by_id(audioFileID)

                if song:
                    responseData = schema.dump(song)

            elif audioFileType == 'podcast':
                schema = PodcastSchema()
                podcast = Podcast.find_by_id(audioFileID)

                if podcast:
                    responseData = schema.dump(podcast)

            elif audioFileType == 'audiobook':
                schema = AudioBookSchema()
                audiobook = AudioBook.find_by_id(audioFileID)

                if audiobook:
                    responseData = schema.dump(audiobook)
            
            if responseData:
                return responseData, 200
            
            logging.warn(f"File with ID: {audioFileID} not found")
            return {'Message': 'File not found'}, 400

        logging.warn(f"AudioFileType or AudioFileID is not validd")
        return {'Message': 'AudioFileType or AudioFileID is not valid'}, 400 

    def put(self, audioFileType, audioFileID):
        if self.isValidInput(audioFileType, audioFileID):
            schema = None
            model = None
            if audioFileType == 'song':
                model = Song
                schema = SongSchema
            elif audioFileType == 'podcast':
                model = Podcast
                schema = PodcastSchema
            elif audioFileType == 'audiobook':
                model = AudioBook
                schema = AudioBookSchema

            data = request.get_json()
            record = model.query.filter_by(id=audioFileID).first()

            if not data:
                return {'Message': 'Request data is invalid'}, 400
            if not record:
                return {'Message': f"No {model.__name__} found with id: {audioFileID}"}, 400

            # Update existing record
            try:
                # Pass ID to update fields for existing records using .update staticmethod for model
                data["id"] = audioFileID
                # schema.load calls post_load which internally calls update class method.
                # update method commits the changes so no need to do it after the load.
                record = schema().load(data, session=db.session, instance=record, partial=True, unknown=EXCLUDE)

            except Exception as e:
                return str(e), 400
            return schema().dump(record), 200

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