from unittest import TestCase
from api.src.models.Participant import Participant

class TestParticipant(TestCase):

    def test_participant_create_object(self):
        participant = Participant("Test")

        self.assertEqual("Test", participant.name)

    def test_participant_repr(self):
        participant = Participant("Test")

        self.assertEqual("Test", participant.__repr__())

    def test_participant_create_object_with_unexpected_argument(self):
        with self.assertRaises(TypeError):
            participant = Participant(name="Test", unexpected=True)
