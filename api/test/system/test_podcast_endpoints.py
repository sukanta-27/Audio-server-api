from api.src.models.Podcast import Podcast, PodcastSchema
from api.src.resources.AudioFileResource import AudioFileResource
from api.src.resources.AudioListResource import AudioListResource
from api.src.resources.CreateAudioResource import CreateAudioResource
from api.test.base_test import BaseTest
import json

class TestPodcastEndpoints(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)

        self.post_data = {
            "audioFileType": "podcast",
            "audioFileMetadata": {
                "name": "Test API Podcast",
                "duration": 360,
                "host": "Robert",
                "participants": [
                    "Rambo"
                ]
            }
        }

        self.update_data = {
            "name": "Updated Test API Podcast",
            "duration": 34223,
            "host": "Sukanta",
            "participants": [
                "Norman"
            ]
        }

        # Create some dummy data
        Podcast("Test 1", 13, "Host 1", ["Participant 1"]).save_to_db()
        Podcast("Test 2", 23, "Host 2", ["Participant 2"]).save_to_db()
   
    def test_post_podcast(self):
        with self.app() as client:
            with self.app_context():
                # Check record named "Test API Podcast" does not exist
                self.assertIsNone(Podcast.find_by_name(self.post_data["audioFileMetadata"]["name"]))
                request = client.post("/", data=json.dumps(self.post_data))

                self.assertEqual(request.status_code, 200)
                self.assertIsNotNone(Podcast.find_by_name(self.post_data["audioFileMetadata"]["name"]))
                self.assertDictEqual(
                    PodcastSchema().dump(Podcast.find_by_name(self.post_data["audioFileMetadata"]["name"])),
                    json.loads(request.data)
                )

    def test_get_podcast(self):
        with self.app() as client:
            with self.app_context():
                test_id = 1
                request = client.get(f"/podcast/{test_id}")

                self.assertEqual(request.status_code, 200)
                self.assertDictEqual(
                    PodcastSchema().dump(Podcast.find_by_id(1)),
                    json.loads(request.data)
                )


    def test_get_podcast_list(self):
        with self.app() as client:
            with self.app_context():
                request = client.get(f"/podcast")

                self.assertEqual(request.status_code, 200)
                json_data = json.loads(request.data)

                self.assertEqual(len(json_data), 2)
                self.assertListEqual(
                    PodcastSchema().dump(Podcast.query.all(), many=True),
                    json_data
                )

    def test_update_podcast(self):
        with self.app() as client:
            with self.app_context():
                test_id = 1
                # Check record exists
                self.assertIsNotNone(Podcast.find_by_id(test_id))

                request = client.put(f"/podcast/{test_id}", \
                    data=json.dumps(self.update_data),\
                    headers={'content-type': 'application/json'})

                self.assertEqual(request.status_code, 200)

                record = Podcast.find_by_id(test_id)

                self.assertIsNotNone(record)
                self.assertDictEqual(
                    PodcastSchema().dump(Podcast.find_by_id(test_id)),
                    json.loads(request.data)
                )
                self.assertEqual(record.name, self.update_data["name"])
                self.assertEqual(record.duration, self.update_data["duration"])
                self.assertEqual(record.host.name, self.update_data["host"])
                self.assertEqual(record.participants[0].name, self.update_data["participants"][0])

    def test_delete_podcast(self):
        with self.app() as client:
            with self.app_context():
                test_id = 1

                # Check record exists before deleting
                self.assertIsNotNone(Podcast.find_by_id(test_id))

                request = client.delete(f"/podcast/{test_id}")

                # Check record doesn't exist after deleting
                self.assertIsNone(Podcast.find_by_id(test_id))
