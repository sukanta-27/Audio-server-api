from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restful import Api
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
Migrate(app, db)

from api.src.resources.AudioFileResource import AudioFileResource
restful_api = Api(app)
restful_api.add_resource(AudioFileResource, '/<string:audioFileType>/<string:audioFileID>')