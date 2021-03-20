from unittest import TestCase
from api.src.models.AudioFile import AudioFile

class TestAudioFile(TestCase):

    def test_create_audiofile_object(self):
        a = AudioFile("Test", 123)

        self.assertEqual("Test", a.name)
        self.assertEqual(123, a.duration)
        self.assertEqual('audiofile', a.audio_type)
        self.assertEqual(None, a.uploaded_time)
        self.assertEqual(None, a.id)
    
    def test_create_audiofile_init_with_unexpected_argument(self):
        with self.assertRaises(TypeError):
            AudioFile("name", duration=22, unexpected=234)
