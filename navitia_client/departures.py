"""
Departures
http://doc.navitia.io/#departures

Also known as /departures service.

This endpoint retrieves a list of departures from a specific datetime of a selected object. Departures are ordered chronologically in ascending order as:


url                                                 Result
/coverage/{region_id}/{resource_path}/departures    List of the next departures, multi-route oriented, only time sorted (no grouped by stop_point/route here)

/coverage/{lon;lat}/coords/{lon;lat}/departures     List of the next departures, multi-route oriented, only time sorted (no grouped by stop_point/route here)
"""
import os


def departures(client, collection_name=None, object_id=None, coords=None, region=None, extra_params=None, verbose=False):
    # Construct url
    if coords and region:
        raise ValueError(
            "Cannot specifiy both coords and region, you must choose one.")
    if coords:
        # TODO: check coords format
        # /coverage/{lon;lat}/coords/{lon;lat}/departures
        url = os.path.join("coverage", coords, "coords",
                           coords, "departures")
    else:
        # /coverage/{region_id}/{resource_path}/departures
        # First choose region
        if not region and not hasattr(client, 'region'):
            raise ValueError(
                "You must specifiy coords or region, either here or in client")
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
        # /coverage/{region_id}/{collection_name}
        if not object_id or not collection_name:
            raise ValueError("of correct type")
        url = os.path.join("coverage", used_region,
                           collection_name, object_id, "departures")

    return client._get(url=url, extra_params=extra_params, verbose=verbose)
