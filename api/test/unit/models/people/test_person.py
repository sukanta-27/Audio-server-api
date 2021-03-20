from unittest import TestCase
from api.src.models.Person import Person

class TestPerson(TestCase):

    def test_person_create_object(self):
        person = Person("Test")

        self.assertEqual("Test", person.name)

    def test_person_repr(self):
        person = Person("Test")

        self.assertEqual("name: Test, type: person", person.__repr__())

    def test_person_create_object_with_unexpected_argument(self):
        with self.assertRaises(TypeError):
            person = Person(name="Test", unexpected=True)
