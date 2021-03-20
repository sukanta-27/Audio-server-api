from unittest import TestCase
from api.src.models.Narrator import Narrator

class TestNarrator(TestCase):

    def test_narrator_create_object(self):
        narrator = Narrator("Test")

        self.assertEqual("Test", narrator.name)

    def test_narrator_repr(self):
        narrator = Narrator("Test")

        self.assertEqual("Test", narrator.__repr__())

    def test_narrator_create_object_with_unexpected_argument(self):
        with self.assertRaises(TypeError):
            narrator = Narrator(name="Test", unexpected=True)
