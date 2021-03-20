from api import db
from api.test.base_test import BaseTest
from api.src.models.AudioBook import AudioBook, AudioBookSchema
from api.src.models.Author import Author
from api.src.models.Narrator import Narrator
from collections import OrderedDict
from marshmallow import ValidationError, EXCLUDE

class TestAudioBookSchema(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)
        self.data = {
            "name": "Test AudioBook",
            "duration": 350,
            "author": "Robert",
            "narrator": "Roy"
        }
        self.schema = AudioBookSchema

    def test_audiobook_dump(self):
        audiobook = AudioBook(
            name="Test",
            duration=33,
            author="Tester",
            narrator="Narrator"
        )
        audiobook.save_to_db()

        # Retrieve DB record for the audiobook created
        audiobook = AudioBook.find_by_name(audiobook.name)
        expected = OrderedDict({
            "id": 1,
            "name": "Test",
            "duration": 33,
            "author": "Tester",
            "narrator": "Narrator",
            "uploaded_time": "T".join(str(audiobook.uploaded_time).split())
        })

        # Get the serialized data
        json_data = self.schema().dump(audiobook)
        self.assertDictEqual(json_data, expected)

    def test_audiobook_load(self):
        audiobook = None

        self.assertIsNone(audiobook)
        audiobook = self.schema().load(self.data, session=db.session, instance=None)
        self.assertIsNotNone(audiobook)

        self.assertEqual(audiobook.name, self.data["name"])
        self.assertEqual(audiobook.duration, self.data["duration"])
        self.assertIsInstance(audiobook.author, Author)
        self.assertIsInstance(audiobook.narrator, Narrator)
        self.assertEqual(audiobook.author.name, self.data["author"])
        self.assertEqual(audiobook.narrator.name, self.data["narrator"])
        self.assertIsNone(audiobook.uploaded_time)
        self.assertIsNone(audiobook.id)


    def test_audiobook_load_name_required(self):
        with self.assertRaises(ValidationError) as e:
            self.data.pop("name")
            audiobook = self.schema().load(self.data, session=db.session)
            self.assertIn(b"'name': ['Missing data for required field.']", str(e))

    def test_audiobook_load_name_char_limit(self):
        # Test load with 0 char in name
        with self.assertRaises(ValidationError) as e:
            self.data["name"] = ""
            audiobook = self.schema().load(self.data, session=db.session)
            self.assertIn(b"'name': ['Length must be between 1 and 100.']", str(e))

        # Test load with 101 char in name
        with self.assertRaises(ValidationError) as e:
            self.data["name"] = "b"*101
            audiobook = self.schema().load(self.data, session=db.session)
            self.assertIn(b"'name': ['Length must be between 1 and 100.']", str(e))

    def test_audiobook_load_duration_required(self):
        with self.assertRaises(ValidationError) as e:
            self.data.pop("duration")
            audiobook = self.schema().load(self.data, session=db.session)
            self.assertIn(b"'duration': ['Missing data for required field.']", str(e))

    def test_audiobook_load_duration_negative_error(self):
        with self.assertRaises(ValidationError) as e:
            self.data["duration"] = -23
            audiobook = self.schema().load(self.data, session=db.session)
            self.assertIn(b"'duration': ['Must be greater than or equal to 0.']", str(e))

    def test_audiobook_load_author_with_101_long_name_error(self):
        self.data["author"] = "b"*101
        with self.assertRaises(ValidationError) as e:
            audiobook = self.schema().load(self.data, session=db.session)
            self.assertIn(b"'author': ['Length must be between 1 and 100.']", error)

    def test_audiobook_load_narrator_with_101_long_name_error(self):
        self.data["narrator"] = "b"*101
        with self.assertRaises(ValidationError) as e:
            audiobook = self.schema().load(self.data, session=db.session)
            self.assertIn(b"'narrator': ['Length must be between 1 and 100.']", error)

    def test_audiobook_load_with_existing_record(self):
        audiobook = self.schema().load(self.data, session=db.session)

        self.assertIsNone(AudioBook.find_by_name(audiobook.name))
        audiobook.save_to_db()
        db_audiobook = AudioBook.find_by_name(audiobook.name)
        self.assertIsNotNone(db_audiobook)

        # load another audiobook with same data and check id is same
        self.data["id"] = db_audiobook.id
        audiobook2 = self.schema().load(self.data, session=db.session,\
             instance=AudioBook.find_by_name(self.data["name"]), unknown=EXCLUDE)

        self.assertIsNotNone(audiobook2)
        self.assertEqual(audiobook2.id, db_audiobook.id)

        

    def tearDown(self):
        BaseTest.tearDown(self)