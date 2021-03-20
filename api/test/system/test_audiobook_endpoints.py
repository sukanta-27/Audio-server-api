from api.src.models.AudioBook import AudioBook, AudioBookSchema
from api.src.resources.AudioFileResource import AudioFileResource
from api.src.resources.AudioListResource import AudioListResource
from api.src.resources.CreateAudioResource import CreateAudioResource
from api.test.base_test import BaseTest
import json

class TestAudioBookEndpoints(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)

        self.post_data = {
            "audioFileType": "audiobook",
            "audioFileMetadata": {
                "name": "Test API AudioBook",
                "duration": 360,
                "author": "Robert",
                "narrator": "Jones"
            }
        }

        self.update_data = {
            "name": "Updated Test API AudioBook",
            "duration": 34223,
            "author": "Martin",
            "narrator": "Fernando"
        }

        # Create some dummy data
        AudioBook("Test 1", 13, "Author 1", "Narrator 1").save_to_db()
        AudioBook("Test 2", 23, "Author 2", "Narrator 2").save_to_db()

    def test_post_audiobook(self):
        with self.app() as client:
            with self.app_context():
                # Check record named "Test API AudioBook" does not exist
                self.assertIsNone(AudioBook.find_by_name(self.post_data["audioFileMetadata"]["name"]))
                request = client.post("/", data=json.dumps(self.post_data))

                self.assertEqual(request.status_code, 200)
                self.assertIsNotNone(AudioBook.find_by_name(self.post_data["audioFileMetadata"]["name"]))
                self.assertDictEqual(
                    AudioBookSchema().dump(AudioBook.find_by_name(self.post_data["audioFileMetadata"]["name"])),
                    json.loads(request.data)
                )

    def test_get_audiobook(self):
        with self.app() as client:
            with self.app_context():
                test_id = 1
                request = client.get(f"/audiobook/{test_id}")

                self.assertEqual(request.status_code, 200)
                self.assertDictEqual(
                    AudioBookSchema().dump(AudioBook.find_by_id(1)),
                    json.loads(request.data)
                )


    def test_get_audiobook_list(self):
        with self.app() as client:
            with self.app_context():
                request = client.get(f"/audiobook")

                self.assertEqual(request.status_code, 200)
                json_data = json.loads(request.data)

                self.assertEqual(len(json_data), 2)
                self.assertListEqual(
                    AudioBookSchema().dump(AudioBook.query.all(), many=True),
                    json_data
                )

    def test_update_audiobook(self):
        with self.app() as client:
            with self.app_context():
                test_id = 1
                # Check record exists
                self.assertIsNotNone(AudioBook.find_by_id(test_id))

                request = client.put(f"/audiobook/{test_id}", \
                    data=json.dumps(self.update_data),\
                    headers={'content-type': 'application/json'})

                self.assertEqual(request.status_code, 200)

                record = AudioBook.find_by_id(test_id)

                self.assertIsNotNone(record)
                self.assertDictEqual(
                    AudioBookSchema().dump(AudioBook.find_by_id(test_id)),
                    json.loads(request.data)
                )
                self.assertEqual(record.name, self.update_data["name"])
                self.assertEqual(record.duration, self.update_data["duration"])
                self.assertEqual(record.author.name, self.update_data["author"])
                self.assertEqual(record.narrator.name, self.update_data["narrator"])

    def test_delete_audiobook(self):
        with self.app() as client:
            with self.app_context():
                test_id = 1

                # Check record exists before deleting
                self.assertIsNotNone(AudioBook.find_by_id(test_id))

                request = client.delete(f"/audiobook/{test_id}")

                # Check record doesn't exist after deleting
                self.assertIsNone(AudioBook.find_by_id(test_id))
