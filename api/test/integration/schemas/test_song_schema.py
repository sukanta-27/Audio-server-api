from api import db
from api.test.base_test import BaseTest
from api.src.models.Song import Song, SongSchema
from collections import OrderedDict
from marshmallow import ValidationError

class TestSongSchema(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)
        self.data = {
            "name": "Test Song",
            "duration": 350
        }
        self.schema = SongSchema

    def test_song_dump(self):
        song = Song(
            name="Test",
            duration=33
        )
        song.save_to_db()

        # Retrieve DB record for the song created
        song = Song.find_by_name(song.name)
        expected = OrderedDict({
            "id": 1,
            "name": "Test",
            "duration": 33,
            "uploaded_time": "T".join(str(song.uploaded_time).split())
        })

        self.assertDictEqual(self.schema().dump(song), expected)

    def test_song_load(self):
        song = None

        self.assertIsNone(song)
        song = self.schema().load(self.data, session=db.session, instance=None)
        self.assertIsNotNone(song)

        self.assertEqual(song.name, self.data["name"])
        self.assertEqual(song.duration, self.data["duration"])
        self.assertIsNone(song.uploaded_time)
        self.assertIsNone(song.id)


    def test_song_load_name_required(self):
        TC_data = self.data.copy()
        with self.assertRaises(ValidationError) as e:
            TC_data.pop("name")
            song = self.schema().load(TC_data, session=db.session)
            self.assertIn(b"'name': ['Missing data for required field.']", str(e))

    def test_song_load_name_char_limit(self):
        TC_data = self.data.copy()

        # Test load with 0 char in name
        with self.assertRaises(ValidationError) as e:
            TC_data["name"] = ""
            song = self.schema().load(TC_data, session=db.session)
            self.assertIn(b"'name': ['Length must be between 1 and 100.']", str(e))

        # Test load with 101 char in name
        with self.assertRaises(ValidationError) as e:
            TC_data["name"] = "b"*101
            song = self.schema().load(TC_data, session=db.session)
            self.assertIn(b"'name': ['Length must be between 1 and 100.']", str(e))

    def test_song_load_duration_required(self):
        TC_data = self.data.copy()
        with self.assertRaises(ValidationError) as e:
            TC_data.pop("duration")
            song = self.schema().load(TC_data, session=db.session)
            self.assertIn(b"'duration': ['Missing data for required field.']", str(e))

    def test_song_load_duration_negative_error(self):
        TC_data = self.data.copy()
        with self.assertRaises(ValidationError) as e:
            TC_data["duration"] = -23
            song = self.schema().load(TC_data, session=db.session)
            self.assertIn(b"'duration': ['Must be greater than or equal to 0.']", str(e))
        

    def tearDown(self):
        BaseTest.tearDown(self)