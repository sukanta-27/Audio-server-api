from unittest import TestCase
from api.src.models.AudioFile import AudioFile

class TestAudioFile(TestCase):

    def test_sanity(self):
        self.assertEqual(2+2, 4)

    def test_create_audiofile_object(self):
        a = AudioFile("Test", 123)

        self.assertEqual("Test", a.name)
        self.assertEqual(123, a.duration)
        self.assertEqual('audiofile', a.audio_type)
        self.assertEqual(None, a.uploaded_time)
        self.assertEqual(None, a.id)
