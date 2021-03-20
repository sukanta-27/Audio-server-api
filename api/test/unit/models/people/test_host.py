from unittest import TestCase
from api.src.models.Host import Host

class TestHost(TestCase):

    def test_host_create_object(self):
        host = Host("Test")

        self.assertEqual("Test", host.name)

    def test_host_repr(self):
        host = Host("Test")

        self.assertEqual("Test", host.__repr__())

    def test_host_create_object_with_unexpected_argument(self):
        with self.assertRaises(TypeError):
            host = Host(name="Test", unexpected=True)
