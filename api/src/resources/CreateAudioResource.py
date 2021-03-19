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
                    db.session.add(record)
                    db.session.commit()
                    return schema.dump(record), 200
            except Exception as e:
                return str(e), 400
        else:
            return {'Message': message}, 400


    def validateJSONData(self, data):
        if 'audioFileType' not in data:
            return False, "Please specify audio file type"
        else:
            if data['audioFileType'] not in ['song', 'podcast', 'audiobook']:
                return False, f"{data['audioFileType']} is not a supported audio type"
        
        if 'audioFileMetadata' not in data:
            return False, "Please specify audio metadata"
        
        return True, "Valid request data"
