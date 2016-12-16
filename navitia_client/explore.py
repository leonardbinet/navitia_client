"""
Public Transportation Objects exploration
http://doc.navitia.io/#public-transportation-objects-exploration

Also known as /networks, /lines, /stop_areas… services.

Once you have selected a region, you can explore the public transportation objects easily with these APIs. You just need to add at the end of your URL a collection name to see every objects within a particular collection. To see an object detail, add the id of this object at the end of the collection’s URL. The paging arguments may be used to paginate results.
Accesses
url                                                 Result
/coverage/{region_id}/{collection_name}             Collection of objects of a region
/coverage/{region_id}/{collection_name}/{object_id} Information about a specific region
/coverage/{lon;lat}/{collection_name}               Collection of objects of a region
/coverage/{lon;lat}/{collection_name}/{object_id}   Information about a specific region

Focus on first two usages (coord service doesn't work for sncf)

Either coords, or region

"""
import os


def explore(client, collection_name, coords=None, region=None, depth=None, distance=None, disable_geojson=None, extra_params=None, specific_object=None, multipage=None, count_per_page=None, page_limit=None, url_suffix=None, verbose=False):

    if specific_object and multipage:
        raise UserWarning("Specific objects return usually one page.")

    # Check accepted_collections
    accepted_collections = {
        "networks",
        "lines",
        "routes",
        "stop_points",
        "stop_areas",
        "commercial_modes",
        "physical_modes",
        "companies",
        "vehicle_journeys",
        "disruptions"
    }
    if collection_name not in accepted_collections:
        raise ValueError("Collection name provided is not supported.")

    # Construct url
    if coords and region:
        raise ValueError(
            "Cannot specifiy both coords and region, you must choose one.")
    if coords:
        # TODO: check coords format
        # /coverage/{lon;lat}/{collection_name}
        url = os.path.join("coverage", coords, collection_name)
    else:
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
        url = os.path.join("coverage", used_region, collection_name)

    # Specific object
    if specific_object:
        url = os.path.join(url, specific_object)

    # Url suffix
    if url_suffix:
        url = os.path.join(url, url_suffix)
    # FILTERS
    # OK: depth, distance, disable_geojson
    # Not taken into account because too specific: odt level, headsign, since
    # / until
    # They can still be taken into account in extra_params argument
    params = {}

    if depth:
        try:
            depth = int(depth)
            params["depth"] = depth
        except ValueError:
            raise ValueError("Depth must be int")

    if distance:
        if not coords:
            raise ValueError("Distance works only with coords")
        try:
            distance = int(distance)
            params["distance"] = distance
        except ValueError:
            raise ValueError("Distance must be int")

    if disable_geojson:
        params["disable_geojson"] = True

    all_params = {**params, **(extra_params or {})}

    if not multipage:
        return client._get(url=url, extra_params=all_params, verbose=verbose)

    else:
        return client._get_multipage(url=url, page_limit=page_limit, count=count_per_page, extra_params=all_params, verbose=verbose)
