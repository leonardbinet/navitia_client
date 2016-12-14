"""
This module computes API requests.
"""
import functools
import os
from datetime import datetime, timedelta
import time

import json
import requests

from multiprocessing import Pool
from navitia_client.utils import important_print
import navitia_client

_RETRIABLE_STATUSES = set([500, 503, 504])


class Client(object):
    """
    Performs requests to the navitia API web services.
    """

    def __init__(self, user, password="", retry_timeout=20, core_url='sncf'):
        if core_url == 'sncf':
            self.core_url = "https://api.sncf.com/v1/"
        else:
            self.core_url = core_url
        self.user = user
        self.password = password
        self.retry_timeout = retry_timeout
        self.last_url = None

    def _get(self, url, extra_params=None, verbose=False, first_request_time=None, retry_counter=0, ignore_fail=False):
        if verbose and not first_request_time:
            print("Import on url %s " % url)

        if not first_request_time:
            first_request_time = datetime.now()

        elapsed = datetime.now() - first_request_time
        if elapsed > timedelta(seconds=self.retry_timeout):
            raise navitia_client.exceptions.Timeout()

        if retry_counter > 0:
            # 0.5 * (1.5 ^ i) is an increased sleep time of 1.5x per iteration,
            # starting at 0.5s when retry_counter=0. The first retry will occur
            # at 1, so subtract that first.
            delay_seconds = 0.5 * 1.5 ** (retry_counter - 1)
            time.sleep(delay_seconds)

        full_url = os.path.join(self.core_url, url)

        try:
            response = requests.get(
                url=full_url, auth=(self.user, self.password), params=(extra_params or {}))

        except requests.exceptions.Timeout:
            if not ignore_fail:
                raise navitia_client.exceptions.Timeout()
            else:
                return False
        except Exception as e:
            if not ignore_fail:
                raise navitia_client.exceptions.TransportError(e)
            else:
                return False

        # Warn if not 200
        if response.status_code != 200:
            print("WARNING: response status_code is %s" % response.status_code)

        if response.status_code in _RETRIABLE_STATUSES:
            # Retry request.
            print("WARNING: retry number %d" % retry_counter)
            return self._get(url=url, extra_params=extra_params, first_request_time=first_request_time, retry_counter=retry_counter + 1, verbose=verbose, ignore_fail=ignore_fail)

        return response

    def _get_single_page_multiprocess(self, url, page, count, extra_params=None, verbose=False):
        """
        Return tuple: (page_number,response)
        Needed to perform multiprocessed requests.
        """
        if verbose:
            print("Import on page %d " % page)
        # Pagination parameters of request
        pagination_params = {
            "start_page": page,
            "count": count,
        }
        parameters = {**pagination_params, **(extra_params or {})}
        # Ignore fail: if one request fails, we still want others to be
        # computed
        response = self._get(
            url=url, extra_params=parameters, ignore_fail=True)

        return (page, response)

    def _extract_nbr_results(self, response):
        """
        Out of a request response, finds total number of results
        """
        parsed = json.loads(response.text)
        try:
            nbr_results = parsed["pagination"]["total_result"]
            return nbr_results
        except KeyError:
            # No pagination in page
            print("WARNING: not able to extract pagination out of first request.")
            return False


def make_api_method(func):
    """
    Provides a single entry point for modifying all API methods.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper

from navitia_client.journeys import journeys
from navitia_client.route_schedules import route_schedules
from navitia_client.multipage import multipage
from navitia_client.raw import raw

Client.journeys = make_api_method(journeys)
Client.route_schedules = make_api_method(route_schedules)
Client.multipage = make_api_method(multipage)
Client.raw = make_api_method(raw)
