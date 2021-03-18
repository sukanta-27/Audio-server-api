from api import db
from api.src.models.AudioFile import AudioFile
from api.src.models.Song import Song
from api.src.models.Podcast import Podcast
from api.src.models.AudioBook import AudioBook

def setup():
	db.drop_all()
	db.create_all()

	s1 = Song('J', 120)
	p1 = Podcast('JRE', 3334, 'Joe Rogan')
	a1 = AudioBook('Hi', 234, 'A', 'B')

	db.session.add(s1)
	db.session.add(p1)
	db.session.add(a1)

	db.session.commit()
