from api.test.base_test import BaseTest
from api.src.models.Podcast import Podcast, PodcastSchema
from api.src.models.Host import Host
from api.src.models.Participant import Participant

class TestPodcast(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)
        
        self.data = {
            "name": "Test Podcast",
            "duration": 300,
            "host": "Robert",
            "participants": [
                "Navin",
                "Sunil",
                "Harshad"
            ]
        }

    def test_create_podcast(self):

        podcast = Podcast(**self.data)

        # Check there is no exisiting podcast named "Test Podcast"
        self.assertIsNone(Podcast.find_by_name(podcast.name))

        # Save podcast to database
        podcast.save_to_db()

        # Check podcast exists
        record = Podcast.find_by_name(podcast.name)
        self.assertIsNotNone(record)
        self.assertIsNotNone(record.id)
        self.assertIsNotNone(record.uploaded_time)
        self.assertEqual(record.name, podcast.name)
        self.assertEqual(record.duration, podcast.duration)

        # check host name and type
        self.assertIsInstance(record.host, Host)
        self.assertEqual(record.host.name, "Robert")
        self.assertEqual(len(record.participants), 3)
        self.assertIsInstance(record.participants[0], Participant)
        self.assertEqual(record.participants[0].name, "Navin")

    def test_get_podcast_by_id_or_name(self):
        # Check a record exists in the db
        podcast = Podcast(**self.data)
        podcast.save_to_db()

        podcast_byname = Podcast.find_by_name(self.data["name"])
        self.assertIsNotNone(podcast_byname)

        id = podcast_byname.id
        
        # Check find_by_id method
        podcast_byid = Podcast.find_by_id(id)
        self.assertIsNotNone(podcast_byid)
        self.assertEqual(podcast_byid.name, podcast_byname.name)
        self.assertEqual(podcast_byid.uploaded_time, podcast_byname.uploaded_time)

    def test_update_podcast(self):
        podcast = Podcast(**self.data)
        podcast.save_to_db()

        # Get the record and check field values
        record = Podcast.find_by_name(self.data["name"])
        self.assertIsNotNone(record)
        self.assertEqual(record.name, self.data["name"])
        self.assertEqual(record.duration, self.data["duration"])

        # Update field values
        update_data = {
            "name": "Updated Test Podcast",
            "duration": 120,
            "host": Host("Updated host"),
            "participants": [
                Participant("Rohan")
            ]
        }
        Podcast.update(update_data, record)

        # Check updated field values
        updated_record = Podcast.find_by_id(record.id)
        self.assertIsNotNone(updated_record)
        self.assertEqual(updated_record.name, update_data["name"])
        self.assertEqual(updated_record.duration, update_data["duration"])
        self.assertIsInstance(updated_record.host, Host)
        self.assertEqual(str(updated_record.host.name), update_data["host"].name)
        self.assertEqual(len(updated_record.participants), 1)
        self.assertEqual(updated_record.participants[0].name, update_data["participants"][0].name)

    def test_delete_podcast(self):
        # Check a record exists in the db
        podcast = Podcast(**self.data)
        podcast.save_to_db()
        self.assertIsNotNone(Podcast.find_by_name(self.data["name"]))

        # Delete podcast
        podcast.delete_from_db()

        # Check record doesn't exist anymore
        self.assertIsNone(Podcast.find_by_name(self.data["name"]))

    
