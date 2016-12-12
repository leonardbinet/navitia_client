#!/usr/bin/python3
import os

from src.client import ApiRequest, RequestParser, etl_sncf
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


etl_sncf(['coverage/sncf/disruptions'], user=USER,
         page_limit=1000, count=300, debug=True)
