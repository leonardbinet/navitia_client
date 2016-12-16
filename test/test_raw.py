"""
Tests for raw request module.

"""

import responses
import time

import navitia_client
import test as _test
import requests


class RawTest(_test.TestCase):

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
    @responses.activate
    def test_extra_params(self):
        responses.add(responses.GET,
                      "https://api.navitia.io/v1/coverage/sncf/disruptions",
                      body='{"status":"OK","results":[]}',
                      status=200,
                      content_type="application/json")
        self.client.raw("coverage/sncf/disruptions",
                        extra_params={"foo": "bar", "yo": "ya"})
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual("https://api.navitia.io/v1/coverage/sncf/disruptions?foo=bar&yo=ya",
                            responses.calls[0].request.url)
