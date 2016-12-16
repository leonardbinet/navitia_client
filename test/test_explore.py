
"""Tests for the object exploration module: explore."""

import responses
# initialize package, and does not mix up names
import test as _test
import navitia_client
import requests


class ExploreTest(_test.TestCase):

    def setUp(self):
        self.user = 'leo'
        self.core_url = "https://api.navitia.io/v1/"
        self.client = navitia_client.Client(self.user)
        self.coords = '2.333333;48.866667'

    def test_non_authorized_ressource(self):
        client = self.client
        client.set_region("sncf")
        false_ressource = 'doesnotexist'
        with self.assertRaises(ValueError):
            client.explore(false_ressource)

    def test_no_region_nor_coords(self):
        # Should raise error if no region nor coords specified
        client = self.client
        ressource = 'disruptions'
        with self.assertRaises(ValueError):
            client.explore(ressource)

    @responses.activate
    def test_explore_ressource_region(self):
        client = self.client
        client.set_region("sncf")
        url = 'https://api.navitia.io/v1/coverage/sncf/disruptions'
        responses.add(responses.GET, url,
                      body='{"disruptions": [], "links": [], "pagination": []}',
                      status=200, content_type='application/json')

        self.client.explore("disruptions")
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(url, responses.calls[0].request.url)

    @responses.activate
    def test_explore_ressource_coords(self):
        client = self.client
        client.set_region("sncf")
        url = 'https://api.navitia.io/v1/coverage/2.333333;48.866667/lines'
        responses.add(responses.GET, url,
                      body='{"disruptions": [], "links": [], "pagination": []}',
                      status=200, content_type='application/json')

        self.client.explore("lines", coords=self.coords, distance=1000)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(url + "?distance=1000",
                            responses.calls[0].request.url)
