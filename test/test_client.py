"""
Tests for client module.

Uses responses package to mock requests package.
https://pypi.python.org/pypi/responses

"""

import responses
import time

import navitia_client
import test as _test
import requests


class ClientTest(_test.TestCase):

    def setUp(self):
        self.user = 'leo'
        self.core_url = "https://api.navitia.io/v1/"
        self.client = navitia_client.Client(self.user)

    @responses.activate
    def test_simple_request(self):
        responses.add(responses.GET,
                      "https://api.navitia.io/v1/coverage/sncf/disruptions",
                      body='yeah',
                      status=200,
                      content_type="application/json")

        self.client.raw("coverage/sncf/disruptions")
        self.assertEqual(1, len(responses.calls))

    # could test retriable status, and parameters
