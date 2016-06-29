import os
import unittest

from w3af_api_client import Connection


class TestBase(unittest.TestCase):
    def setUp(self):
        host = os.environ.get('W3AF_HOST', 'localhost')
        port = os.environ.get('W3AF_PORT', 5000)
        self.targets = os.environ.get('W3AF_TARGETS', 'http://localhost').split(',')

        self.connection = Connection('http://{}:{}/'.format(host, port))

    @classmethod
    def _get_profile(cls, name):
        with open('tests/data/' + name) as f:
            return f.read()
