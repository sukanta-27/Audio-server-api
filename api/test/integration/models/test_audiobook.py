from api.test.base_test import BaseTest
from api.src.models.AudioBook import AudioBook, AudioBookSchema
from api.src.models.Author import Author
from api.src.models.Narrator import Narrator

class TestAudioBook(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)
        
        self.data = {
            "name": "Test AudioBook",
            "duration": 300,
            "author": "Robert",
            "narrator": "Navin"
        }

    def test_create_audiobook(self):

        audiobook = AudioBook(**self.data)

        # Check there is no exisiting audiobook named "Test AudioBook"
        self.assertIsNone(AudioBook.find_by_name(audiobook.name))

        # Save audiobook to database
        audiobook.save_to_db()

        # Check audiobook exists
        record = AudioBook.find_by_name(audiobook.name)
        self.assertIsNotNone(record)
        self.assertIsNotNone(record.id)
        self.assertIsNotNone(record.uploaded_time)
        self.assertEqual(record.name, audiobook.name)
        self.assertEqual(record.duration, audiobook.duration)

        # check author name and type
        self.assertIsInstance(record.author, Author)
        self.assertEqual(record.author.name, self.data["author"])
        self.assertIsInstance(record.narrator, Narrator)
        self.assertEqual(record.narrator.name, self.data["narrator"])

    def test_get_audiobook_by_id_or_name(self):
        # Check a record exists in the db
        audiobook = AudioBook(**self.data)
        audiobook.save_to_db()

        audiobook_byname = AudioBook.find_by_name(self.data["name"])
        self.assertIsNotNone(audiobook_byname)

        id = audiobook_byname.id
        
        # Check find_by_id method
        audiobook_byid = AudioBook.find_by_id(id)
        self.assertIsNotNone(audiobook_byid)
        self.assertEqual(audiobook_byid.name, audiobook_byname.name)
        self.assertEqual(audiobook_byid.uploaded_time, audiobook_byname.uploaded_time)

    def test_update_audiobook(self):
        audiobook = AudioBook(**self.data)
        audiobook.save_to_db()

        # Get the record and check field values
        record = AudioBook.find_by_name(self.data["name"])
        self.assertIsNotNone(record)
        self.assertEqual(record.name, self.data["name"])
        self.assertEqual(record.duration, self.data["duration"])

        # Update field values
        update_data = {
            "name": "Updated Test AudioBook",
            "duration": 120,
            "author": Author("Updated author"),
            "narrator": Narrator("Updated Narrator")
        }
        AudioBook.update(update_data, record)

        # Check updated field values
        updated_record = AudioBook.find_by_id(record.id)
        self.assertIsNotNone(updated_record)
        self.assertEqual(updated_record.name, update_data["name"])
        self.assertEqual(updated_record.duration, update_data["duration"])
        self.assertIsInstance(updated_record.author, Author)
        self.assertEqual(str(updated_record.author.name), update_data["author"].name)
        self.assertEqual(updated_record.narrator.name, update_data["narrator"].name)

    def test_delete_audiobook(self):
        # Check a record exists in the db
        audiobook = AudioBook(**self.data)
        audiobook.save_to_db()
        self.assertIsNotNone(AudioBook.find_by_name(self.data["name"]))

        # Delete audiobook
        audiobook.delete_from_db()

        # Check record doesn't exist anymore
        self.assertIsNone(AudioBook.find_by_name(self.data["name"]))

    
