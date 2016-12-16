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

    def __init__(self, user, password="", retry_timeout=20, core_url='https://api.navitia.io/v1/', region=None):
        self.core_url = core_url
        self.user = user
        self.password = password
        self.retry_timeout = retry_timeout
        self.requested_urls = []
        if region:
            self.region = region

    def set_region(self, region):
        if not isinstance(region, str):
            raise ValueError("Region must be a string")
        self.region = region

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
            self.requested_urls.append(response.url)

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
        # Verbose for first page only
        if page != 0:
            verbose = False
        response = self._get(
            url=url, extra_params=parameters, ignore_fail=True, verbose=verbose)

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

    def _get_multipage(self, url, page_limit=10, count=100, extra_params=None, verbose=False, log=False):
        """
        url: str
        #

        page_limit: int
        #

        count: int
        #

        extra_params: dict
        #

        verbose: boolean
        #

        log: boolean
        #

        ############
        return: dict
            key: page number
            value: response object
        """
        responses = {}

        # First page
        page, response = self._get_single_page_multiprocess(
            url=url, page=0, count=count, verbose=verbose, extra_params=extra_params)
        responses[page] = response

        # Find number of requests to make
        nbr_results = self._extract_nbr_results(responses[0])
        if not nbr_results:
            # If unable to get pagination count, returns first response
            return responses

        # Find number of pages to query
        blocs = nbr_results // count
        page_limit = min(page_limit, blocs + 1)
        if verbose:
            important_print("There are %d elements with %d elements per page. Limit is %d." % (
                nbr_results, count, page_limit))

        # Query other pages, multiprocessing
        pages = range(1, page_limit)
        pool = Pool(processes=30)
        n = len(pages)
        all_parameters = zip([self] * n, [url] * n,
                             pages, [count] * n, [extra_params or {}] * n, [verbose] * n)

        list_tuples = pool.map(unwrap_self, all_parameters)
        pool.close()
        pool.join()
        # Add results to initial results (first page)
        responses.update(dict(list_tuples).items())

        # Save logs
        if log:
            log = {}
            log["date"] = str(datetime.now().isoformat())
            log["url"] = url
            log["count_per_page"] = count
            log["page_limit"] = page_limit
            log["nbr_results"] = nbr_results
            responses["log"] = log
        if verbose:
            print("Multipage finished")
        return responses


def unwrap_self(arg, **kwarg):
    """ To unwrap self in multiprocessing mode
    http://www.rueckstiess.net/research/snippets/show/ca1d7d90
    """
    return Client._get_single_page_multiprocess(*arg, **kwarg)


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
from navitia_client.raw import raw
from navitia_client.inverted_geocoding import inverted_geocoding
from navitia_client.explore import explore
from navitia_client.departures import departures

Client.journeys = make_api_method(journeys)
Client.route_schedules = make_api_method(route_schedules)
Client.raw = make_api_method(raw)
Client.inverted_geocoding = make_api_method(inverted_geocoding)
Client.explore = make_api_method(explore)
Client.departures = make_api_method(departures)
