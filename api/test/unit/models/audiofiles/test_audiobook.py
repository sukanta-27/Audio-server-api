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
        test = AudioBook("name", 12, "author", "narrator")

        self.assertEqual(
            "name: name, Audio type: audiobook, Author: author, narrator: narrator",
            test.__repr__()
        )

    def test_audioBook_without_author_error(self):
        with self.assertRaises(TypeError) as e:
            test = AudioBook(name="Test", duration=12, narrator="ss")

            self.assertIn(
                b"A required field does not have the correct type",
                str(e)
            )

    def test_audioBook_without_narrator_error(self):
        with self.assertRaises(TypeError) as e:
            test = AudioBook(name="Test", duration=12, author="ss")

            self.assertIn(
                b"A required field does not have the correct type",
                str(e)
            )
            
    def test_audioBook_create_object_with_host_object(self):
        author = Author("Test Author")
        test = AudioBook(name="Test", duration=12, author=author, narrator="Narrator")

        self.assertEqual("Test", test.name)
        self.assertEqual(12, test.duration)
        self.assertIsInstance(test.author, Author)
        self.assertEqual("Test Author", test.author.name)
        self.assertIsInstance(test.narrator, Narrator)
        self.assertEqual("Narrator", test.narrator.name)

    def test_audioBook_create_object_with_host_object(self):
        narrator = Narrator("Test Narrator")
        test = AudioBook(name="Test", duration=12, author="Author", narrator=narrator)

        self.assertEqual("Test", test.name)
        self.assertEqual(12, test.duration)
        self.assertIsInstance(test.author, Author)
        self.assertEqual("Author", test.author.name)
        self.assertIsInstance(test.narrator, Narrator)
        self.assertEqual("Test Narrator", test.narrator.name)

    def test_audioBook_create_object_with_str_duration_error(self):
        with self.assertRaises(TypeError) as e:
            test = AudioBook("name", "12", author="tester", narrator="narrator")
            self.assertIn(b"A required field does not have the correct type", str(e))

