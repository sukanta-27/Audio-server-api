from api import db
from api.test.base_test import BaseTest
from api.src.models.Podcast import Podcast, PodcastSchema
from api.src.models.Host import Host
from api.src.models.Participant import Participant
from collections import OrderedDict
from marshmallow import ValidationError, EXCLUDE

class TestPodcastSchema(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)
        self.data = {
            "name": "Test Podcast",
            "duration": 350,
            "host": "Robert",
            "participants": [
                "Ram",
                "Rahim"
            ]
        }
        self.schema = PodcastSchema

    def test_podcast_dump(self):
        podcast = Podcast(
            name="Test",
            duration=33,
            host="Tester",
            participants=["A", "B"]
        )
        podcast.save_to_db()

        # Retrieve DB record for the podcast created
        podcast = Podcast.find_by_name(podcast.name)
        expected = OrderedDict({
            "id": 1,
            "name": "Test",
            "duration": 33,
            "host": "Tester",
            "participants": ["A", "B"],
            "uploaded_time": "T".join(str(podcast.uploaded_time).split())
        })

        # Get the serialized data
        json_data = self.schema().dump(podcast)

        # Separate out participant lists from json_data and expected data to compare separately
        participantList = json_data.pop("participants")
        expectedParticipantList = expected.pop("participants")

        self.assertDictEqual(json_data, expected)
        self.assertCountEqual(participantList, expectedParticipantList)

    def test_podcast_load(self):
        podcast = None

        self.assertIsNone(podcast)
        podcast = self.schema().load(self.data, session=db.session, instance=None)
        self.assertIsNotNone(podcast)

        self.assertEqual(podcast.name, self.data["name"])
        self.assertEqual(podcast.duration, self.data["duration"])
        self.assertIsNone(podcast.uploaded_time)
        self.assertIsNone(podcast.id)


    def test_podcast_load_name_required(self):
        TC_data = self.data.copy()
        with self.assertRaises(ValidationError) as e:
            TC_data.pop("name")
            podcast = self.schema().load(TC_data, session=db.session)
            self.assertIn(b"'name': ['Missing data for required field.']", str(e))

    def test_podcast_load_name_char_limit(self):
        TC_data = self.data.copy()

        # Test load with 0 char in name
        with self.assertRaises(ValidationError) as e:
            TC_data["name"] = ""
            podcast = self.schema().load(TC_data, session=db.session)
            self.assertIn(b"'name': ['Length must be between 1 and 100.']", str(e))

        # Test load with 101 char in name
        with self.assertRaises(ValidationError) as e:
            TC_data["name"] = "b"*101
            podcast = self.schema().load(TC_data, session=db.session)
            self.assertIn(b"'name': ['Length must be between 1 and 100.']", str(e))

    def test_podcast_load_duration_required(self):
        TC_data = self.data.copy()
        with self.assertRaises(ValidationError) as e:
            TC_data.pop("duration")
            podcast = self.schema().load(TC_data, session=db.session)
            self.assertIn(b"'duration': ['Missing data for required field.']", str(e))

    def test_podcast_load_duration_negative_error(self):
        TC_data = self.data.copy()
        with self.assertRaises(ValidationError) as e:
            TC_data["duration"] = -23
            podcast = self.schema().load(TC_data, session=db.session)
            self.assertIn(b"'duration': ['Must be greater than or equal to 0.']", str(e))

    def test_podcast_load_host_with_101_long_name_error(self):
        self.data["host"] = "b"*101
        error = None
        with self.assertRaises(ValidationError) as e:
            podcast = self.schema().load(self.data, session=db.session)
            self.assertIn(b"'host': ['Length must be between 1 and 100.']", error)

    def test_podcast_load_with_11_participants_error(self):
        self.data["participants"] = [str(i) for i in range(11)]
        with self.assertRaises(ValidationError) as e:
            podcast = self.schema().load(self.data, session=db.session)
            self.assertIn(b"['Podcast can not have more than 10 participants']", str(e))

    def test_podcast_load_with_existing_record(self):
        podcast = self.schema().load(self.data, session=db.session)

        self.assertIsNone(Podcast.find_by_name(podcast.name))
        podcast.save_to_db()
        db_podcast = Podcast.find_by_name(podcast.name)
        self.assertIsNotNone(db_podcast)

        # load another podcast with same data and check id is same
        self.data["id"] = db_podcast.id
        podcast2 = self.schema().load(self.data, session=db.session,\
             instance=Podcast.find_by_name(self.data["name"]), unknown=EXCLUDE)
        db.session.commit()

        self.assertIsNotNone(podcast2)
        self.assertEqual(podcast2.id, db_podcast.id)

        

    def tearDown(self):
        BaseTest.tearDown(self)