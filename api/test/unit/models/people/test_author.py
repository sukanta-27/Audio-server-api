from unittest import TestCase
from api.src.models.Author import Author

class TestAuthor(TestCase):

    def test_author_create_object(self):
        author = Author("Test")

        self.assertEqual("Test", author.name)

    def test_author_repr(self):
        author = Author("Test")

        self.assertEqual("Test", author.__repr__())

    def test_author_create_object_with_unexpected_argument(self):
        with self.assertRaises(TypeError):
            author = Author(name="Test", unexpected=True)
