from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from .config import Config

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