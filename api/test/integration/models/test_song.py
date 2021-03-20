from ..base_test import BaseTest
from api.src.models.Song import Song, SongSchema

class TestSong(BaseTest):

    def test_create_song(self):
        song = Song(name="Test Song", duration=300)

        # Check there is no exisiting song named "Test Song"
        self.assertIsNone(Song.find_by_name(song.name))

        # Save song to database
        song.save_to_db()

        # Check song exists
        record = Song.find_by_name(song.name)
        self.assertIsNotNone(record)
        self.assertIsNotNone(record.id)
        self.assertIsNotNone(record.uploaded_time)
        self.assertEqual(record.name, song.name)
        self.assertEqual(record.duration, song.duration)

    def test_get_song_by_id(self):
        # Check a record exists in the db
        Song("Test song", 123).save_to_db()
        song = Song.query.first()
        self.assertIsNotNone(song)

        id = song.id
        
        # Check find_by_id method
        record = Song.find_by_id(id)
        self.assertIsNotNone(record)
        self.assertEqual(record.name, song.name)
        self.assertEqual(record.uploaded_time, song.uploaded_time)

    def test_update_song(self):
        song = Song("Test song", 123)
        song.save_to_db()

        # Get the record and check field values
        record = Song.find_by_name("Test song")
        self.assertIsNotNone(record)
        self.assertEqual(record.name, "Test song")
        self.assertEqual(record.duration, 123)

        # Update field values
        data = {
            "name": "Updated Test Song",
            "duration": 300
        }
        Song.update(data, record)

        # Check updated field values
        updated_record = Song.find_by_id(record.id)
        self.assertIsNotNone(updated_record)
        self.assertEqual(updated_record.name, "Updated Test Song")
        self.assertEqual(updated_record.duration, 300)


    def test_delete_song(self):
        # Check a record exists in the db
        song = Song("Test song", 123)
        song.save_to_db()
        self.assertIsNotNone(Song.find_by_name("Test song"))

        # Delete song
        song.delete_from_db()

        # Check record doesn't exist anymore
        self.assertIsNone(Song.find_by_name("Test song"))

    
