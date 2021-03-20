from unittest import TestCase
from api.src.models.Podcast import Podcast
from api.src.models.Host import Host
from api.src.models.Participant import Participant
from marshmallow import ValidationError

class TestPodcast(TestCase):

    def test_podcast_create_object(self):
        test = Podcast(
            name="Test",
            duration=3600,
            host="Tester",
            participants=["One", "Two"]
        )

        self.assertEqual("Test", test.name)
        self.assertEqual(3600, test.duration)
        self.assertIsInstance(test.host, Host)
        self.assertEqual("Tester", test.host.name)
        self.assertIsInstance(test.participants, list)
        self.assertEqual(2, len(test.participants))
        self.assertIsInstance(test.participants[0], Participant)
        self.assertEqual("One", test.participants[0].name)

    def test_podcast_repr(self):
        test = Podcast("name", 12, "ss", ["ab", "cd", "ef"])

        self.assertEqual(
            "name: name, Audio type: podcast, Host:ss, participants: [ab, cd, ef]",
            test.__repr__()
        )

    def test_podcast_participants_list_optional(self):
        test = Podcast("Test", 12, "ss")

        self.assertEqual(
            "name: Test, Audio type: podcast, Host:ss, participants: []",
            test.__repr__()
        )
        self.assertCountEqual([], test.participants)

    def test_podcast_create_object_with_11_participants_error(self):
        with self.assertRaises(ValidationError) as e:
            test = Podcast("name", 12, host="ss", \
                participants=["ab", "cd", "ef", "a", "c", "b", "w", "wx", "xxx", "xcv", "xc"])
            self.assertIn(b"Podcast cannot have more than 10 participants", str(e))

    def test_podcast_create_object_without_host_error(self):
        with self.assertRaises(TypeError) as e:
            test = Podcast("name", 12, participants=["ab"])
            self.assertIn(b"__init__() missing 1 required positional argument: 'host'", str(e))

    def test_podcast_create_object_with_str_duration_error(self):
        with self.assertRaises(TypeError) as e:
            test = Podcast("name", "12", host="tester", participants=["ab"])
            self.assertIn(b"A required field does not have the correct type", str(e))

