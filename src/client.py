"""
This module computes API requests.
"""
import functools
import os
import json
import requests
import pandas as pd

from datetime import datetime
from multiprocessing import Pool
from src.utils import flatten_dataframe, important_print


def etl_sncf(api_paths, user, page_limit=100, count=100, debug=False):
    """
    Take a list of paths to extract, and save all data in subfolder.
    """
    for requested_path in api_paths:
        # Create Data directory if it doesn't exist
        directory = os.path.join("Data", requested_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Compute request
        request = Client(user, requested_path)
        request._get_multiple_pages(
            page_limit=page_limit, debug=debug, count=count)
        print(request.total_result)
        # Write request log
        request.write_log(directory)
        if not request.first_request_status:
            # If first request failed, no parsing, go to next element
            request.write_log(directory)
            continue
        # Parse results if sucessful
        parser = RequestParser(request.results, requested_path)
        parser.parse()
        # Print some information
        parser.explain()
        # Write it on disk
        parser.write_all(directory)

# http://www.rueckstiess.net/research/snippets/show/ca1d7d90


def unwrap_self_f(arg, **kwarg):
    """ For multiprocessing
    """
    return Client._get_single_page(*arg, **kwarg)


class Client(object):
    """
    Performs requests to the navitia API web services.
    """

    def __init__(self, user, path):
        self.core_path = "https://api.sncf.com/v1/"
        self.user = user
        self.path = os.path.join(self.core_path, path)
        # Here are stored all requests results
        self.results = {}
        self.parsed_results = {}
        self.first_request_status = False
        self.total_result = False
        self.log = None
        self.count_per_page = None
        self.page_limit = None
        important_print("Computing API request for " + self.path, 1)

    def _get_single_page(self, page=0, debug=False, count=100):
        if debug:
            print("Import on page " + str(page))
        # Pagination parameters of request
        payload = {
            "start_page": page,
            "count": count,
        }
        # Compute request
        request_result = requests.get(
            url=self.path, auth=(self.user, ""), params=payload)
        # Save result
        self.results[page] = request_result
        # Save result success, and number of results, for first page.
        if request_result.status_code == 200 and page == 0:
            self.first_request_status = True
            self.extract_nbr_results()
        return (page, request_result)

    def extract_nbr_results(self):
        if not self.first_request_status:
            print("Cannot extract, because no successful request.")
        # Parse first request answer.
        parsed = json.loads(self.results[0].text)
        # Extract pagination part.
        pagination = parsed["pagination"]
        # Extract total_result
        self.total_result = pagination["total_result"]

    def _get_multiple_pages(self, page_limit=10, debug=False, count=100):
        # TODO manage failed requests
        # Compute first with 100 lines
        self.page_limit = page_limit
        self.count_per_page = count
        self._get_single_page(0, debug=True, count=count)
        if not self.total_result and not self.first_request_status:
            print("Fail, cound not successfully compute first request.")
        # Find number of requests to make
        blocs = self.total_result // count
        page_limit = min(page_limit, blocs + 1)
        if debug:
            important_print("There are " + str(self.total_result) + " elements with " +
                            str(count) + " elements per page. Limit is " + str(page_limit) + ".")
        # Compute necessary queries
        # Here multiprocessing
        pages = range(1, page_limit)
        pool = Pool(processes=30)
        list_tuples = pool.map(unwrap_self_f, zip(
            [self] * len(pages), pages, [debug] * len(pages), [count] * len(pages)))
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


def make_api_method(func):
    """
    Provides a single entry point for modifying all API methods.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper


class RequestParser:

    def __init__(self, request_results, asked_path):
        self.asked_path = asked_path
        self.results = request_results
        self.item_name = os.path.basename(asked_path)
        self.parsed = {}  # dictionary of page : dictionary
        self.parsing_errors = {}
        self.nested_items = None  # will be a dict
        self.unnested_items = None  # will be a dict
        self.links = []  # first page is enough
        self.disruptions = {}  # all pages
        self.keys = []  # collect keys found in request answer
        self.nbr_expected_items = None
        self.nbr_collected_items = None
        self.log = None

    def set_results(self, request_results):
        self.results = request_results

    def parse(self):
        self.parse_requests()
        self.extract_keys()
        self.extract_links()
        self.extract_disruptions()
        self.get_nested_items()
        self.get_unnested_items()
        self.extract_nbr_expected_items()
        self.count_nbr_collected_items()
        self.parse_log()

    def parse_requests(self):
        # First operation, to parse requests text into python dictionnaries
        for page, value in self.results.items():
            # Only add if answer was good
            if value.status_code == 200:
                try:
                    self.parsed[page] = json.loads(value.text)
                except ValueError:
                    print("JSON decoding error.")
                    self.parsing_errors[page] = "JSON decoding error"

    def get_nested_items(self):
        """
        Result is a dictionary, of one key: item_name, and value is list of items (concatenate all result pages).
        """
        dictionnary = {self.item_name: []}
        for page, value in self.parsed.items():
            # concatenate two lists of items
            dictionnary[self.item_name] += value[self.item_name]
        self.nested_items = dictionnary

    def get_nested_disruptions(self):
        """
        Result is a dictionary, of one key: item_name, and value is list of items (concatenate all result pages).
        """
        if self.item_name == "disruptions":
            return False

        dictionnary = {"disruptions": []}
        for page, value in self.parsed.items():
            # concatenate two lists of items
            dictionnary["disruptions"] += value["disruptions"]
        self.disruptions = dictionnary

    def get_unnested_items(self):
        df = pd.DataFrame(self.nested_items[self.item_name])
        flatten_dataframe(df, drop=True, max_depth=5)
        self.unnested_items = df.to_dict()

    def extract_keys(self):
        # Extract keys of first page
        self.keys = list(self.parsed[0].keys())

    def extract_links(self):
        # Extract from first page
        try:
            self.links = self.parsed[0]["links"]
        except KeyError:
            self.links = {"links": "Not found"}

    def extract_disruptions(self):
        # TODO extract all pages
        # Extract from first page
        try:
            self.disruptions = self.parsed[0]["disruptions"]
        except KeyError:
            self.disruptions = {"disruptions": "Not found"}

    def extract_nbr_expected_items(self):
        if self.results[0].status_code != 200:
            return None
        # Parse first request answer.
        parsed = json.loads(self.results[0].text)
        # Extract pagination part.
        pagination = parsed["pagination"]
        # Extract total_result
        self.nbr_expected_items = pagination["total_result"]

    def count_nbr_collected_items(self):
        unnested = pd.DataFrame(self.unnested_items)  # df
        self.nbr_collected_items = len(unnested.index)

    def explain(self):
        print("Parsing:")
        print("Keys found: " + str(self.keys))
        print(self.item_name.capitalize() + " has " +
              str(self.nbr_expected_items) + " elements.")

    def parse_log(self):
        log = {}
        log["number_requests"] = len(self.results)
        log["number_parsed"] = len(self.parsed)
        log["keys"] = self.keys
        log["nbr_announced_items"] = self.nbr_expected_items
        log["nbr_collected_items"] = self.nbr_collected_items
        log["item_columns"] = list(pd.DataFrame(
            self.unnested_items).columns.values)
        self.log = log
        log["parsing_errors"] = self.parsing_errors

    def write_all(self, directory):
        # Get results
        unnested = pd.DataFrame(self.unnested_items)  # df
        nested = self.nested_items  # dict
        # Write item csv
        unnested.to_csv(os.path.join(directory, self.item_name + ".csv"))
        # Write item json
        with open(os.path.join(directory, self.item_name + ".json"), 'w') as f:
            json.dump(nested, f, ensure_ascii=False)
        # Write links (of first page)
        with open(os.path.join(directory, "links.json"), 'w') as f:
            json.dump(self.links, f, ensure_ascii=False)
        # Write disruptions (if item different)
        if self.item_name != "disruptions":
            unnested_dis = pd.DataFrame(self.disruptions)  # df
            unnested_dis.to_csv(os.path.join(directory, "disruptions.csv"))
        # Write logs
        with open(os.path.join(directory, "parse_log.json"), 'w') as f:
            json.dump(self.log, f, ensure_ascii=False)
