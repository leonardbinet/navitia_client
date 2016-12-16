
"""Tests for the route_schedules module."""

import responses
# initialize test package __init__, and does not mix up names
import test as _test
import navitia_client
import requests


class RouteSchedulesTest(_test.TestCase):

    def setUp(self):
        self.user = 'leo'
        self.core_url = "https://api.navitia.io/v1/"
        self.client = navitia_client.Client(self.user)
        self.coords = '2.333333;48.866667'
        self.datetime = '20161221T000000'

    def test_no_region(self):
        # Should fail, needs one region
        client = self.client
        with self.assertRaises(ValueError):
            client.route_schedules(raw="anything")

    def test_wrong_datafreshness(self):
        # Should fail, only base_schedule or realtime
        client = self.client
        client.set_region("sncf")
        with self.assertRaises(ValueError):
            client.route_schedules(raw="anything", data_freshness="lalala")

    def test_multiple_ressources_arguments(self):
        # Should fail, only one accepted out of line, raw, route etc..
        client = self.client
        client.set_region("sncf")
        with self.assertRaises(ValueError):
            client.route_schedules(raw="anything", line="line")
