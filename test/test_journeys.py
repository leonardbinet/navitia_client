
"""Tests for the journeys module."""

import responses
# initialize test package __init__, and does not mix up names
import test as _test
import navitia_client
import requests


class JourneysTest(_test.TestCase):

    def setUp(self):
        self.user = 'leo'
        self.core_url = "https://api.navitia.io/v1/"
        self.client = navitia_client.Client(self.user)
        self.lat = '48.866667'
        self.lon = '2.333333'
        self.coords = '2.333333;48.866667'
        self.datetime = '20161221T000000'

    def test_no_region(self):
        # Should fail, needs one region
        client = self.client
        with self.assertRaises(ValueError):
            client.journeys(origin=self.coords)

    def test_wrong_datetime_represents(self):
        # Should fail, only departure or arrival
        client = self.client
        client.set_region("sncf")
        with self.assertRaises(ValueError):
            client.journeys(
                origin=self.coords, datetime=self.datetime, datetime_represents="lalala")

    def test_datetime_represents_without_datetime(self):
        # Should fail, datetime_represents needs datetime
        client = self.client
        client.set_region("sncf")
        with self.assertRaises(ValueError):
            client.journeys(origin=self.coords, datetime_represents="lalala")

    def test_wrong_datafreshness(self):
        # Should fail, only base_schedule or realtime
        client = self.client
        client.set_region("sncf")
        with self.assertRaises(ValueError):
            client.journeys(origin=self.coords, data_freshness="lalala")
