from unittest import TestCase
from api.src.models.Song import Song

class TestSong(TestCase):

    def test_create_song_object(self):
        a = Song("Test", 123)

        self.assertEqual("Test", a.name)
        self.assertEqual(123, a.duration)
        self.assertEqual('song', a.audio_type)
        self.assertEqual(None, a.uploaded_time)
        self.assertEqual(None, a.id)
    
    def test_create_song_init_with_unexpected_argument(self):
        with self.assertRaises(TypeError):
            Song("name", duration=22, unexpected=234)

    def test_song_repr(self):
        song = Song("Test", 300)

        self.assertEqual(
            "name: Test, Audio type: song, Uploaded:None",
            song.__repr__()
        )