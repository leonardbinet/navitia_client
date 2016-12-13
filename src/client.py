"""
This module computes API requests.
"""
import functools
import os
from datetime import datetime
import time

import json
import requests

from multiprocessing import Pool
from src.utils import important_print
import src


_RETRIABLE_STATUSES = set([500, 503, 504])


class Client(object):
    """
    Performs requests to the navitia API web services.
    """

    def __init__(self, user, retry_timeout=20):
        self.core_path = "https://api.sncf.com/v1/"
        self.user = user
        self.retry_timeout = retry_timeout

        self.path = None
        # Result: [page, result]
        self.results = {}
        self.parsed_results = {}
        self.first_request_status = False
        self.total_result = False

        self.log = None

        # For multiple pages requests
        self.count_per_page = None
        self.page_limit = None

    def _get(self, url, extra_params=None, verbose=False, first_request_time=None, retry_counter=0):
        if verbose and not first_request_time:
            print("Import on url %s " % url)

        if not first_request_time:
            first_request_time = datetime.now()

        elapsed = datetime.now() - first_request_time
        if elapsed > self.retry_timeout:
            raise src.exceptions.Timeout()

        if retry_counter > 0:
            # 0.5 * (1.5 ^ i) is an increased sleep time of 1.5x per iteration,
            # starting at 0.5s when retry_counter=0. The first retry will occur
            # at 1, so subtract that first.
            delay_seconds = 0.5 * 1.5 ** (retry_counter - 1)
            time.sleep(delay_seconds)

        full_url = os.path.join(self.core_path, url)
        try:
            response = requests.get(
                url=full_url, auth=(self.user, ""), params=(extra_params or {}))
        except requests.exceptions.Timeout:
            raise src.exceptions.Timeout()
        except Exception as e:
            raise src.exceptions.TransportError(e)
        # Warn if not 200
        if response.status_code != 200:
            print("Warning: response status_code is %s" % response.status_code)

        if response.status_code in _RETRIABLE_STATUSES:
            # Retry request.
            return self._get(url=url, extra_params=extra_params, first_request_time=first_request_time, retry_counter=retry_counter + 1, verbose=verbose)

        # Return raw response object
        return response

    def _get_single_page_multiprocess(self, path, page, count, extra_params=None, extract_pagination=False, verbose=False):

        if verbose:
            print("Import on page %d " % page)
        # Pagination parameters of request
        pagination_params = {
            "start_page": page,
            "count": count,
        }
        parameters = {**pagination_params, **(extra_params or {})}
        full_path = os.path.join(self.core_path, path)
        response = requests.get(
            url=full_path, auth=(self.user, ""), params=parameters)

        # Warn if not 200
        if response.status_code != 200:
            print("Warning: response status_code is %s" % response.status_code)

        # Save result
        self.results[page] = response

        # Save result success, and number of results, for first page.
        if extract_pagination:
            if response.status_code != 200:
                raise ValueError("Request failed for pagination")
            else:
                self.first_request_status = True
                self._extract_nbr_results()
        return (page, response)

    def _extract_nbr_results(self):
        # Parse first request answer.
        parsed = json.loads(self.results[0].text)
        # Extract pagination part.
        try:
            pagination = parsed["pagination"]
            self.total_result = pagination["total_result"]
        except KeyError:
            # No pagination in page
            self.total_result = False

    def _get_multiple_pages(self, path, page_limit=10, count=100, extra_params=None, verbose=False):
        # TODO manage failed requests
        # Compute first with 100 lines
        self.page_limit = page_limit
        self.count_per_page = count
        self._get_single_page_multiprocess(path=path, page=0, count=count,
                                           verbose=True, extract_pagination=True)

        # Find number of requests to make
        blocs = self.total_result // count
        page_limit = min(page_limit, blocs + 1)

        if verbose:
            important_print("There are " + str(self.total_result) + " elements with " +
                            str(count) + " elements per page. Limit is " + str(page_limit) + ".")
        # Compute necessary queries
        # Here multiprocessing
        pages = range(1, page_limit)
        pool = Pool(processes=30)
        n = len(pages)
        all_parameters = zip([self] * n, [path] * n,
                             pages * n, [count] * n, [extra_params or {}] * n)

        list_tuples = pool.map(unwrap_self_f, all_parameters)
        pool.close()
        pool.join()

        # Add results to initial results (first page)
        self.results.update(dict(list_tuples).items())

        # Save logs
        self.requests_log()

    def explain(self):
        print("Detailed results")
        # TODO

    def requests_log(self):
        log = {}
        log["date"] = str(datetime.now().isoformat())
        status_codes = {k: v.status_code for k, v in self.results.items()}
        log["status_codes"] = status_codes
        log["path"] = self.path
        log["count_per_page"] = self.count_per_page
        log["page_limit"] = self.page_limit
        log["total_result"] = self.total_result
        self.log = log

    def write_log(self, directory):
        with open(os.path.join(directory, "requests_log.json"), 'w') as f:
            json.dump(self.log, f, ensure_ascii=False)


# http://www.rueckstiess.net/research/snippets/show/ca1d7d90
def unwrap_self_f(arg, **kwarg):
    """ For multiprocessing
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

from src.journeys import journeys

Client.journeys = make_api_method(journeys)
