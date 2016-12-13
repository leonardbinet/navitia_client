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

## USAGE
You first have to ask for an API key (for instance SNCF), and store it at the root of the repository within a secret.json file, like this:
```
 {
     "USER": "your_api_user"
 }
```
This is made to not save one's API key on github (in .gitignore).

Then to launch functions, you have to call them from the main function.
This architecture is easier because of python import system.

### Extract data from API:
You can simply launch the main module, and it will get data from the api and save csv files in a Data folder.
