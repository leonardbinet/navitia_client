#!/usr/bin/python3

from src.client import Client
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


coords = [48.846905, 2.377097]
coords = '2.377097;48.846905'
raw_url = 'coverage/sncf/stop_points/stop_point:OCE:SP:CorailIntercit%C3%A9-87116137/places_nearby'
stop_area = 'stop_area:OCE:SA:87171009'
stop_point = "stop_point:OCE:SP:CorailIntercité-87113001"
isodate = '20161221T000000'

client = Client(USER)
response1 = client.journeys(origin=stop_area, verbose=True)
response2 = client.route_schedules(stop_point=stop_point, verbose=True)
response3 = client.raw(url=raw_url)

url = 'coverage/sncf/disruptions'
multi_response = client.multipage(
    page_limit=10, url=url, verbose=True)
