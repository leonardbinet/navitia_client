# Python Client for Navitia Services

## NAVITIA OVERVIEW
navitia.io is the open API for building cool stuff with mobility data. It provides the following services

- journeys computation
- line schedules
- next departures
- exploration of public transport data / search places
- and sexy things such as isochrones


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
client = Client(user=USER)

raw_url = 'coverage/sncf/stop_points/stop_point:OCE:SP:CorailIntercit%C3%A9-87116137/places_nearby'
stop_area = 'stop_area:OCE:SA:87171009'
stop_point = "stop_point:OCE:SP:CorailIntercité-87113001"

response1 = client.journeys(origin=from_area)
response2 = client.route_schedules(stop_point=stop_point)
response3 = client.raw(url=raw_url)
```
## METHODS
Client class has multiple methods:
- Client.raw() : when you want to choose freely url and parameters, and still benefit from core functionalities
- Client.mulipage() : parallelized requests for multi-pages ressources.
- Client.journey() : computes journeys
- Client.route_schedules() : computes route_schedules

And many more to come:
- isochrones
- departures
- arrivals
- many others...

## MISCELLANEOUS
- verbose=True parameter if you want to get information in console about requests.
- client.requested_urls attribute if you want to see all urls requested by your client.
