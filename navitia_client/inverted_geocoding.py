"""
http://doc.navitia.io/#inverted-geocoding
Also known as /coords service.

Very simple service: you give Navitia some coordinates, it answers you

    your detailed postal address
    the right Navitia “coverage” which allows you to access to all known local mobility services


Accesses
url                                        Result
coords/{lon;lat}                           Detailed address point
coverage/{region_id}/coords/{lon;lat}      Detailed address point

You can also combine /coords with other filter as :

    get POIs near a coordinate
        https://api.navitia.io/v1/coverage/fr-idf/coords/2.377310;48.847002/pois?distance=1000
    get specific POIs near a coordinate
        https://api.navitia.io/v1/coverage/fr-idf/poi_types/poi_type:amenity:bicycle_rental/coords/2.377310;48.847002/pois?distance=1000

"""
import os


def inverted_geocoding(client, coords=None, lat=None, lon=None, pois=None, distance=None, region=None, verbose=False):

    # By default do not use region: coords/{lon;lat}
    if not region:
        base_url = "coords"

    # Else: coverage/{region_id}/coords/{lon;lat}
    else:
        if region == True:
            if not hasattr(client, 'region'):
                raise ValueError(
                    "You must specifiy region, either here or in client")
            else:
                used_region = client.region

        elif isinstance(region, str):
            # maybe check
            used_region = region

        base_url = os.path.join("coverage", used_region, "coords")

    extra_params = {}

    # coords, or lat and lon
    arg_count = sum(1 for x in [coords, lat and lon] if x)
    if arg_count != 1:
        raise ValueError(
            "Needs coords, or latitude and longitude.")

    if coords:
        # TODO check if coords ok
        url = os.path.join(base_url, coords)

    if lat and lon:
        # TODO check if lat and lon ok
        url = os.path.join(base_url, str(lon) + ";" + str(lat))

    if pois:
        # TODO check if pois ok
        url = os.path.join(url, "pois")

    if distance:
        # TODO check distance
        extra_params["distance"] = distance
    return client._get(url=url, extra_params=extra_params, verbose=verbose)
