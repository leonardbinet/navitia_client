import os
import json
import pandas as pd
from navitia_client.utils import flatten_dataframe, important_print


class Parser:

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
