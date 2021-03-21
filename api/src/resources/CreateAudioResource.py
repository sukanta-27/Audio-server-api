import logging
from api import db
from flask import request
from flask_restful import Resource
from api.src.models.Song import Song, SongSchema
from api.src.models.Podcast import Podcast, PodcastSchema
from api.src.models.AudioBook import AudioBook, AudioBookSchema

class CreateAudioResource(Resource):

    def post(self):
        data = request.get_json(force=True)
        isValid, message = self.validateJSONData(data)

        if isValid:
            schema = None
            if data['audioFileType'] == 'song':
                schema = SongSchema()
            elif data['audioFileType'] == 'podcast':
                schema = PodcastSchema()
            elif data['audioFileType'] == 'audiobook':
                schema = AudioBookSchema()

            try:
                record = schema.load(data['audioFileMetadata'], session=db.session)
                if record:
                    record.save_to_db()
                    logging.info(f"{record.name} saved to database")
                    return schema.dump(record), 200
            except Exception as e:
                logging.warn("There was an problem in creating the record")
                return str(e), 400
        else:
            return {'Message': message}, 400


    def validateJSONData(self, data):
        if 'audioFileType' not in data:
            logging.warn("Audio file type not given in request")
            return False, "Please specify audio file type"
        else:
            if data['audioFileType'] not in ['song', 'podcast', 'audiobook']:
                logging.warn(f"{data['audioFileType']} is not a supported audio type")
                return False, f"{data['audioFileType']} is not a supported audio type"
        
        if 'audioFileMetadata' not in data:
            logging.warn("Audio Metadata not given in request")
            return False, "Please specify audio metadata"
        
        return True, "Valid request data"
