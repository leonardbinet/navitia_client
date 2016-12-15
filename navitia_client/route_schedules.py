# http://doc.navitia.io/#route-schedules
"""
Also known as /route_schedules service.

This endpoint gives you access to schedules of routes (so a kind of time table), with a response made of an array of route_schedule, and another one of note. You can access it via that kind of url: https://api.navitia.io/v1/{a_path_to_a_resource}/route_schedules

URLs:
/coverage/{region_id}/{resource_path}/route_schedules

trips:
/coverage/sncf/trips/{trip_id}/route_schedules
/coverage/{lon;lat}/coords/{lon;lat}/route_schedules

stop_points
/coverage/sncf/stop_points/stop_point:OCE:SP:CorailIntercit%C3%A9-87116137/route_schedules

routes
/coverage/sncf/routes/route:OCE:1-TrainTER-87471003-87474007/route_schedules

lines
coverage/sncf/lines/line:OCE:SN-87775866-87775007/route_schedules
"""

import os


def route_schedules(client, raw=None, line=None, route=None, trip=None, stop_point=None, from_datetime=None, duration=None, items_per_schedule=None, data_freshness=None, disable_geojson=None, region=None, verbose=False):
    """
    from_datetime: iso-date-time
    # The date_time from which you want the schedules

    duration : int
    # Maximum duration in seconds between from_datetime and the retrieved datetimes. (default in api: 86400)

    items_per_schedule: int
    # Maximum number of columns per schedule.

    data_freshness: enum
    # Define the freshness of data to use
        - realtime
        - base_schedule (default)

        disable_geojson: boolean
    # Default false

    """
    params = {}

    # Region selection
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
        used_region = client.region
    else:
        # shouldn't be possible
        raise ValueError("Weird error, caused by region")

    url_begin = os.path.join("coverage", used_region)
    url_end = "route_schedules"

    # Maximum one, out of: trip, stop_point, route, line, raw
    # Minimum one
    arg_count = sum(1 for x in [raw, trip, stop_point, route, line] if x)
    if arg_count != 1:
        raise ValueError(
            "Needs at least, and at most one argument among raw, trip, stop_point, route, line.")

    if raw:
        # /coverage/sncf/routes/route:OCE:1-TrainTER-87471003-87474007/route_schedules
        # raw = "routes/route:OCE:1-TrainTER-87471003-87474007/"
        # made for all use cases
        full_url = os.path.join(url_begin, raw, url_end)

    if route:
        # /coverage/sncf/routes/route:OCE:1-TrainTER-87471003-87474007/route_schedules
        full_url = os.path.join(url_begin, "routes", route, url_end)

    if trip:
        # /coverage/sncf/trips/{trip_id}/route_schedules
        # check trip_id format?
        full_url = os.path.join(url_begin, "trips", trip, url_end)

    if stop_point:
        # /coverage/sncf/stop_points/stop_point:OCE:SP:CorailIntercit%C3%A9-87116137/route_schedules
        # check id format?
        full_url = os.path.join(url_begin, "stop_points", stop_point, url_end)

    if line:
        # coverage/sncf/lines/line:OCE:SN-87775866-87775007/route_schedules
        # check id format?
        full_url = os.path.join(url_begin, "lines", line, url_end)

    if from_datetime:
        # TODO: check is well formated
        params["from_datetime"] = from_datetime

    if duration:
        if isinstance(duration, int):
            params["duration"] = duration
        else:
            raise ValueError("Duration should be integer")

    if data_freshness in [None, "realtime", "base_schedule"]:
        params["data_freshness"] = data_freshness
    else:
        raise ValueError(
            "Data freshness if specified must be 'realtime' or 'base_schedule'")

    if isinstance(items_per_schedule, int):
        params["items_per_schedule"] = items_per_schedule

    if disable_geojson:
        params["disable_geojson"] = True

    return client._get(url=full_url, extra_params=params, verbose=verbose)
