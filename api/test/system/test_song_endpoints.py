from api.src.models.Song import Song, SongSchema
from api.src.resources.AudioFileResource import AudioFileResource
from api.src.resources.AudioListResource import AudioListResource
from api.src.resources.CreateAudioResource import CreateAudioResource
from api.test.base_test import BaseTest
import json

class TestSongEndpoints(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)

        self.post_data = {
            "audioFileType": "song",
            "audioFileMetadata": {
                "name": "Test API Song",
                "duration": 360
            }
        }

        self.update_data = {
            "name": "Updated Test API Song",
            "duration": 34223
        }
   
        # Create some dummy data for testing
        Song("Test 1", 100).save_to_db()
        Song("Test 2", 200).save_to_db()

    def test_post_song(self):
        with self.app() as client:
            with self.app_context():
                # Check record named "Test API Song" does not exist
                self.assertIsNone(Song.find_by_name(self.post_data["audioFileMetadata"]["name"]))
                request = client.post("/", data=json.dumps(self.post_data))

                self.assertEqual(request.status_code, 200)
                self.assertIsNotNone(Song.find_by_name(self.post_data["audioFileMetadata"]["name"]))
                self.assertDictEqual(
                    SongSchema().dump(Song.find_by_name(self.post_data["audioFileMetadata"]["name"])),
                    json.loads(request.data)
                )

    def test_get_song(self):
        with self.app() as client:
            with self.app_context():
                test_id = 1
                request = client.get(f"/song/{test_id}")

                self.assertEqual(request.status_code, 200)
                self.assertDictEqual(
                    SongSchema().dump(Song.find_by_id(1)),
                    json.loads(request.data)
                )

    def test_get_song_list(self):
        with self.app() as client:
            with self.app_context():
                request = client.get(f"/song")

                self.assertEqual(request.status_code, 200)
                json_data = json.loads(request.data)

                self.assertEqual(len(json_data), 2)
                self.assertListEqual(
                    SongSchema().dump(Song.query.all(), many=True),
                    json_data
                )

    def test_update_song(self):
        with self.app() as client:
            with self.app_context():
                test_id = 1
                # Check record exists
                self.assertIsNotNone(Song.find_by_id(test_id))

                request = client.put(f"/song/{test_id}", \
                    data=json.dumps(self.update_data),\
                    headers={'content-type': 'application/json'})

                self.assertEqual(request.status_code, 200)

                record = Song.find_by_id(test_id)

                self.assertIsNotNone(record)
                self.assertDictEqual(
                    SongSchema().dump(Song.find_by_id(test_id)),
                    json.loads(request.data)
                )
                self.assertEqual(record.name, self.update_data["name"])
                self.assertEqual(record.duration, self.update_data["duration"])

    def test_delete_song(self):
        with self.app() as client:
            with self.app_context():
                test_id = 1

                # Check record exists before deleting
                self.assertIsNotNone(Song.find_by_id(test_id))

                request = client.delete(f"/song/{test_id}")

                # Check record doesn't exist after deleting
                self.assertIsNone(Song.find_by_id(test_id))
