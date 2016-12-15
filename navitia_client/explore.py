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

"""
import os


def explore(client, collection_name, region=None, extra_params=None, verbose=False):

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
    # /coverage/{region_id}/{collection_name}
    url = os.path.join("coverage", used_region, collection_name)

    # Parameters TODO
    # depth, odt level, distance, headsign,since / until,disable_geojson,Filter

    return client._get(url=url, extra_params=extra_params, verbose=verbose)
