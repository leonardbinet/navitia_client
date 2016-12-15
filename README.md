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
You first have to ask for an API key (for instance SNCF). Suppose you have it.

```
from navitia_client import Client
client = Client(user=USER, core_url='https://api.sncf.com/v1/')
client.set_region("sncf")

# Get all journeys from a given point or ressource:
stop_area = 'stop_area:OCE:SA:87171009'
response1 = client.journeys(origin=stop_area)

# Get route_schedules for given stop point:
stop_point = "stop_point:OCE:SP:CorailIntercité-87113001"
response2 = client.route_schedules(stop_point=stop_point)

# Compute a custom request (raw_url, and extra_params):
raw_url = 'coverage/sncf/stop_points/stop_point:OCE:SP:CorailIntercit%C3%A9-87116137/places_nearby'
response3 = client.raw(url=raw_url)

# Compute multi-pages request:
url = 'coverage/sncf/disruptions'
multi_response = client.multipage(page_limit=10, url=url)
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
