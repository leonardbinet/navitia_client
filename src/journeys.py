"""Performs requests to the Google Maps Directions API."""


def journeys(client, origin=None, destination=None, datetime=None, datetime_represents=None, data_freshness=None):
    """
    from:
    # The id of the departure of your journey. If none are provided an isochrone is computed

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

    # checks if good format for from and to

    params = {}

    if not origin and not destination:
        raise ValueError("Must specify at least origin or destination")

    if origin:
        params["from"] = origin

    if destination:
        params["to"] = destination

    # checks if datetime format is good

    if datetime:
        params["datetime"] = datetime

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

    return client._get(path="coverage/sncf/journeys", extra_params=params)
