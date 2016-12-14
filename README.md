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
client = Client(user=USER)

raw_url = 'coverage/sncf/stop_points/stop_point:OCE:SP:CorailIntercit%C3%A9-87116137/places_nearby'
from_area = 'stop_area:OCE:SA:87171009'
stop_point = "stop_point:OCE:SP:CorailIntercité-87113001"

response1 = client.journeys(origin=from_area, verbose=True)
response2 = client.route_schedules(stop_point=stop_point, verbose=True)
response3 = client.raw(url=raw_url)
```
