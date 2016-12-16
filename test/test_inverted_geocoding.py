
"""Tests for the inverted-geocoding module."""

import responses
# initialize test package __init__, and does not mix up names
import test as _test
import navitia_client
import requests


class InvertedGeocodingTest(_test.TestCase):

    def setUp(self):
        self.user = 'leo'
        self.core_url = "https://api.navitia.io/v1/"
        self.client = navitia_client.Client(self.user)
        self.lat = '48.866667'
        self.lon = '2.333333'
        self.coords = '2.333333;48.866667'

    def test_latlon_and_coords(self):
        # Should fail, need one or the other
        client = self.client
        with self.assertRaises(ValueError):
            client.inverted_geocoding(
                lat=self.lat, lon=self.lon, coords=self.coords)
        # another try with region given, should fail as well
        client.set_region("sncf")
        with self.assertRaises(ValueError):
            client.inverted_geocoding(
                lat=self.lat, lon=self.lon, coords=self.coords)

    @responses.activate
    def test_coords_request(self):
        # Without region: should work: coords/{lon;lat}
        client = self.client
        url1 = "https://api.navitia.io/v1/coords/2.333333;48.866667"
        responses.add(responses.GET, url1,
                      body='yo',
                      status=200, content_type='application/json')
        client.inverted_geocoding(coords=self.coords)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(url1, responses.calls[0].request.url)

        # With region: should work: coverage/{region_id}/coords/{lon;lat}
        client.set_region("sncf")
        url2 = "https://api.navitia.io/v1/coverage/sncf/coords/2.333333;48.866667"
        responses.add(responses.GET, url2,
                      body='yo',
                      status=200, content_type='application/json')
        client.inverted_geocoding(coords=self.coords, region=True)
        self.assertEqual(2, len(responses.calls))
        self.assertURLEqual(url2, responses.calls[1].request.url)

    @responses.activate
    def test_lat_lon_request(self):
        # Without region: should work: coords/{lon;lat}
        client = self.client
        url1 = "https://api.navitia.io/v1/coords/2.333333;48.866667"
        responses.add(responses.GET, url1,
                      body='yo',
                      status=200, content_type='application/json')
        client.inverted_geocoding(lat=self.lat, lon=self.lon)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(url1, responses.calls[0].request.url)

        # With region: should work: coverage/{region_id}/coords/{lon;lat}
        client.set_region("sncf")
        url2 = "https://api.navitia.io/v1/coverage/sncf/coords/2.333333;48.866667"
        responses.add(responses.GET, url2,
                      body='yo',
                      status=200, content_type='application/json')
        client.inverted_geocoding(lat=self.lat, lon=self.lon, region=True)
        self.assertEqual(2, len(responses.calls))
        self.assertURLEqual(url2, responses.calls[1].request.url)
