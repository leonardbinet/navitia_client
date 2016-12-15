"""Performs multi-pages requests to the Navitia journeys API.

The requests are parallelized to reduce significantly the request time.

Most useful with:
- connections (walking connections between stop_points?)
- disruptions (trip disruptions, one-to-one relationship with trips)
- journey_pattern_points
- journey_patterns
- lines
- routes
- stop_areas (area of aggregation of stop_points)
- stop_points (where journeys can stop)
- trips
- vehicle_journeys
"""

from navitia_client.client import Client
from navitia_client.utils import important_print
from multiprocessing import Pool
from datetime import datetime


def unwrap_self(arg, **kwarg):
    """ To unwrap self in multiprocessing mode
    http://www.rueckstiess.net/research/snippets/show/ca1d7d90
    """
    return Client._get_single_page_multiprocess(*arg, **kwarg)


def multipage(client, url, page_limit=10, count=100, extra_params=None, verbose=False, log=False):
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
    page, response = client._get_single_page_multiprocess(
        url=url, page=0, count=count, verbose=verbose, extra_params=extra_params)
    responses[page] = response

    # Find number of requests to make
    nbr_results = client._extract_nbr_results(responses[0])
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
    all_parameters = zip([client] * n, [url] * n,
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
