from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restful import Api
from .config import Config
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
Migrate(app, db)

from api.src.models.AudioFile import AudioFile
from api.src.models.Song import Song
from api.src.models.Podcast import Podcast
from api.src.models.AudioBook import AudioBook
from api.src.models.Person import Person
from api.src.models.Host import Host
from api.src.models.Participant import Participant
from api.src.models.Author import Author
from api.src.models.Narrator import Narrator

from api.src.resources.AudioFileResource import AudioFileResource
from api.src.resources.CreateAudioResource import CreateAudioResource
from api.src.resources.AudioListResource import AudioListResource

restful_api = Api(app)
restful_api.add_resource(CreateAudioResource, '/')
restful_api.add_resource(AudioListResource, '/<string:audioFileType>')
restful_api.add_resource(AudioFileResource, '/<string:audioFileType>/<string:audioFileID>')

# Add Index route so show documentation
@app.route("/")
def index():
    return render_template('index.html')
