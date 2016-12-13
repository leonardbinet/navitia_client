#!/usr/bin/python3
import os

from src.client import Client
from src.parser import Parser
from configuration import USER

# All main requests (missing some)
api_paths_list = [
    'coverage/sncf/addresses',
    'coverage/sncf/contributors',
    'coverage/sncf/companies',
    'coverage/sncf/connections',
    'coverage/sncf/vehicle_journeys',  # flatten diff keys?
    'coverage/sncf/networks',
    'coverage/sncf/commercial_modes',
    'coverage/sncf/physical_modes',
    'coverage/sncf/disruptions',
    'coverage/sncf/pois',
    'coverage/sncf/stop_points',
    'coverage/sncf/poi_types',
    'coverage/sncf/datasets',
    'coverage/sncf/journey_pattern_points',
    'coverage/sncf/lines',
    'coverage/sncf/coord',
    'coverage/sncf/stop_areas',
    'coverage/sncf/coords',
    'coverage/sncf/journey_patterns',
    'coverage/sncf/routes',
    'coverage/sncf/trips',
    'coverage/sncf/line_groups',
    'coverage/sncf/places',
    'coverage/sncf/journeys'
]


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
        request = Client(user)
        request._get_multiple_pages(
            page_limit=page_limit, count=count, path=requested_path, verbose=True)
        print(request.total_result)
        # Write request log
        request.write_log(directory)
        if not request.first_request_status:
            # If first request failed, no parsing, go to next element
            request.write_log(directory)
            continue
        # Parse results if sucessful
        parser = Parser(request.results, requested_path)
        parser.parse()
        # Print some information
        parser.explain()
        # Write it on disk
        parser.write_all(directory)

coords = [48.846905, 2.377097]
etl_sncf(['coverage/sncf/disruptions'], user=USER,
         page_limit=10, count=50, debug=True)

from_area = 'stop_area:SNF:SA:PARISMONT'
to_area = 'stop_area:SNF:SA:NANTES'
from_area = 'stop_area:OCE:SA:87171009'


client = Client(USER, "coverage/sncf/journeys")
#client._get_single_page(extra_params={"from": from_area})
# client.journeys(origin=from_area)
