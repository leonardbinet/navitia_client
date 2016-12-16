# Python Client for Navitia Services

## NAVITIA OVERVIEW
[Navitia](http://navitia.io/) is the open API for building cool stuff with mobility data. It provides the following services

- journeys computation
- line schedules
- next departures
- exploration of public transport data / search places
- and sexy things such as isochrones

You can find the documentation [here](http://doc.navitia.io/).

## GOAL
The goal of this package is to provide a dead simple way to request navitia's API.

## INSTALLATION
To install package:
```
pip install navitia_client
```

## USAGE
You first have to ask for an API key, for Navitia API, you can get it [here](https://www.navitia.io/register/). Suppose you have it:

```
from navitia_client import Client

client = Client(user=NAVITIA_USER)
client.set_region("fr-idf")

# Get all journeys from a given point or ressource:
stop_area = "stop_area:OIF:SA:8768138"
response1 = client.journeys(origin=stop_area, verbose=True)

# Get route_schedules for given stop point:
stop_point = "stop_point:OIF:SP:10:1145"
response2 = client.route_schedules(stop_point=stop_point, verbose=True)

# Compute a custom request (raw_url, and extra_params):
raw_url = 'coverage/fr-idf/stop_areas/stop_area:OIF:SA:8768138/places_nearby'
response3 = client.raw(url=raw_url, verbose=True)

# Compute custom multi-pages request:
url = 'coverage/fr-idf/lines'
response4 = client.raw(url, multipage=True, page_limit=10, verbose=True)

# Compute invert geocoding request:
lat = '48.866667'
lon = '2.333333'
response5 = client.inverted_geocoding(lat=lat, lon=lon, verbose=True)

# Compute explore ressource request, single or multipage:
response6 = client.explore("networks", verbose=True)
response7 = client.explore("lines", multipage=True, page_limit=5, count_per_page=50, verbose=True)
```
## METHODS

http://doc.navitia.io/#api-catalog

Client class has multiple methods:
- Client.raw() : when you want to choose freely url and parameters, and still benefit from core functionalities
- Client.multipage() : parallelized requests for multi-pages ressources.
- Client.journeys() : computes journeys
- Client.route_schedules() : computes route_schedules

And many more to come:
- isochrones
- departures
- arrivals
- many others...

## MISCELLANEOUS
- verbose=True parameter if you want to get information in console about requests.
- client.requested_urls attribute if you want to see all urls requested by your client.

## TODO

### CLEAN REPO:
- unit tests
- code documentation with sphynx

### ADD METHODS

All api points: http://doc.navitia.io/#api-catalog :

- Coverage - ok
- Datasets - ok
- Contributors - ok
- Inverted geocoding - ok
- Public Transportation Objects exploration - ok
- Autocomplete on Public Transport objects - todo
- Autocomplete on geographical objects - todo
- Places Nearby - todo
- Journeys - to finish
- Isochrones (currently in Beta) - todo
- Route Schedules - to finish
- Stop Schedules - todo
- Departures - todo
- Arrivals - todo
- Traffic reports - todo
