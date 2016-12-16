"""Performs requests to the Navitia journeys API.
http://doc.navitia.io/#journeys

Two accesses:
/coverage/{region_id}/journeys 	List of journeys on a specific coverage
/coverage/{a_path_to_resource}/journeys

Focus on first access:
# from/to parameters
##coordonates: lon;lat
- coverage/sncf/journeys?from=2.3749036;48.8467927&to=2.2922926;48.8583736&
- coverage/sncf/journeys?from=2.3749036%3B48.8467927&to=2.2922926%3B48.8583736&
##ressources id:
- coverage/sncf/journeys?from=stop_point:OCE:SP:CorailIntercit%C3%A9-87113001
- coverage/sncf/journeys?from=stop_area:OCE:SA:87171009
# datetime parameter:
&datetime=20161221T000000
"""

import os


def journeys(client, origin=None, destination=None, datetime=None, datetime_represents=None, data_freshness=None, region=None, verbose=False):
    """
    from:
    # The id of the departure of your journey. If none are provided an isochrone is computed, can be:
        - a ressource id:
        - coordonates, lon;lat:


    to:
    # The id of the arrival of your journey. If none are provided an isochrone is computed

    datetime:
    # Date and time to go: iso-date-time

    datetime_represents:
    # Can be departure or arrival.
    # If departure, the request will retrieve journeys starting after datetime.
    # If arrival it will retrieve journeys arriving before datetime.

    data_freshness:
    #Define the freshness of data to use to compute journeys
        - realtime
        - base_schedule
    when using the following parameter “&data_freshness=base_schedule”
    you can get disrupted journeys in the response. You can then display the disruption message to the traveler and make a realtime request to get a new undisrupted solution.

    """

    # First choose region
    if not region and not hasattr(client, 'region'):
        raise ValueError(
            "You must specifiy region, either here or in client")

    elif region:
        if isinstance(region, str):
            # region argument overrides client specified region
            used_region = region
        else:
            raise ValueError("Region must be a string")

    elif not region and hasattr(client, 'region'):
        # Takes already specified region
        used_region = client.region

    else:
        # shouldn't be possible
        raise ValueError("Weird error, caused by region")

    # checks if good format for 'from' and 'to'
    params = {}

    url = os.path.join("coverage", used_region, "journeys")

    if not origin and not destination:
        raise UserWarning(
            "Must specify at least origin or destination, or else it will return an isochrone")

    if origin:
        params["from"] = origin

    if destination:
        params["to"] = destination

    # checks if datetime format is good

    if datetime:
        params["datetime"] = datetime

    if not datetime and datetime_represents:
        raise ValueError(
            "You need to specify datetime when datetime_represents is used.")

    if datetime_represents in [None, "departure", "arrival"]:
        params["datetime_represents"] = datetime_represents
    else:
        raise ValueError(
            "datetime_represents if specified must be 'departure' or 'arrival'")

    if data_freshness in [None, "realtime", "base_schedule"]:
        params["data_freshness"] = data_freshness
    else:
        raise ValueError(
            "Data freshness if specified must be 'realtime' or 'base_schedule'")

    return client._get(url=url, extra_params=params, verbose=verbose)
