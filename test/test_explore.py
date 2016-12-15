
"""Tests for the object exploration module: explore."""

import responses
# initialize package, and does not mix up names
import test as _test
import navitia_client
import requests


class ExploreTest(_test.TestCase):

    def setUp(self):
        self.user = 'leo'
        self.core_url = "https://api.sncf.com/v1/"
        self.client = navitia_client.Client(self.user)

    def test_non_authorized_ressource(self):
        client = self.client
        client.set_region("sncf")
        false_ressource = 'doesnotexist'
        with self.assertRaises(ValueError):
            client.explore(false_ressource)

    def test_no_region(self):
        # Should raise error if no region specified
        client = self.client
        ressource = 'disruptions'
        with self.assertRaises(ValueError):
            client.explore(ressource)

    @responses.activate
    def test_explore_ressource(self):
        client = self.client
        client.set_region("sncf")
        url = 'https://api.sncf.com/v1/coverage/sncf/disruptions'
        responses.add(responses.GET, url,
                      body='{"disruptions": [], "links": [], "pagination": []}',
                      status=200, content_type='application/json')

        self.client.explore("disruptions")
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(url, responses.calls[0].request.url)
