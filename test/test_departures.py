
"""Tests for the object departures module."""

import responses
# initialize package, and does not mix up names
import test as _test
import navitia_client
import requests


class DeparturesTest(_test.TestCase):

    def setUp(self):
        self.user = 'leo'
        self.core_url = "https://api.navitia.io/v1/"
        self.client = navitia_client.Client(self.user)
        self.coords = '2.333333;48.866667'

    def test_no_region_nor_coords(self):
        # Should raise error if no region nor coords specified
        pass
