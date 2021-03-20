from unittest import TestCase
from api.src.models.AudioBook import AudioBook
from api.src.models.Author import Author
from api.src.models.Narrator import Narrator
from api.src.models.Participant import Participant
from marshmallow import ValidationError

class TestAudioBook(TestCase):

    def test_audioBook_create_object(self):
        test = AudioBook(
            name="Test",
            duration=3600,
            author="TesterAuthor",
            narrator="TesterNarrator"
        )

        self.assertEqual("Test", test.name)
        self.assertEqual(3600, test.duration)
        self.assertIsInstance(test.author, Author)
        self.assertEqual("TesterAuthor", test.author.name)
        self.assertIsInstance(test.narrator, Narrator)
        self.assertEqual("TesterNarrator", test.narrator.name)

    def test_audioBook_repr(self):
        test = AudioBook("name", 12, "ss", ["ab", "cd", "ef"])

        self.assertEqual(
            "name: name, Audio type: audioBook, Host:ss, participants: [ab, cd, ef]",
            test.__repr__()
        )

    def test_audioBook_participants_list_optional(self):
        test = AudioBook("Test", 12, "ss")

        self.assertEqual(
            "name: Test, Audio type: audioBook, Host:ss, participants: []",
            test.__repr__()
        )
        self.assertCountEqual([], test.participants)

    def test_audioBook_create_object_with_11_participants_error(self):
        with self.assertRaises(ValidationError) as e:
            test = AudioBook("name", 12, host="ss", \
                participants=["ab", "cd", "ef", "a", "c", "b", "w", "wx", "xxx", "xcv", "xc"])
            self.assertIn(b"AudioBook cannot have more than 10 participants", str(e))

    def test_audioBook_create_object_without_host_error(self):
        with self.assertRaises(TypeError) as e:
            test = AudioBook("name", 12, participants=["ab"])
            self.assertIn(b"__init__() missing 1 required positional argument: 'host'", str(e))

    def test_audioBook_create_object_with_str_duration_error(self):
        with self.assertRaises(TypeError) as e:
            test = AudioBook("name", "12", host="tester", participants=["ab"])
            self.assertIn(b"A required field does not have the correct type", str(e))

