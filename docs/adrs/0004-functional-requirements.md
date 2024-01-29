# Functional requirements

Date: `2023-11-22`

## Status

Accepted

## Context

Need to define requirements.

## Decision

We want to achieve following functionalities:
- Authentication system features
  - Plain
  - [OAuth](https://github.com/jazzband/django-oauth-toolkit)
  - Password reset via email
    - Needs to be customized and use [django-mailer](https://github.com/pinax/django-mailer/blob/master/docs/usage.rst#usage)
    package in order to increase safety
  - [2FA](https://django-two-factor-auth.readthedocs.io/en/1.15.5/)
    - Think how it ties in with both OAuth and plain authentication systems

- Main business functionalities
  - Users should be able to add locations (geolocations/places) to their account's dashboard
  - Supported ways of searching for locations:
    - A search box allowing search by name (should give many possibilities in case of some possible phrases)
    - A search box allowing search by geolocation returning several closest locations
    - **Bonus** - search by geolocation derived from user's clicking on the interactive world map
      (`geoJSON` format with countries' borders)
      - Would look great, but might be hard to implement
    - Above methods would be powered by [Geocoding API](https://openweathermap.org/api/geocoding-api)

  - Dashboard should allow users to see current weather parameters as well as the forecast as defined
    in the Free tier of [Open Weather API](https://openweathermap.org/price)
  - In addition to weather data, users could access air pollution information (current + forecast from [Air Pollution API](https://openweathermap.org/api/air-pollution))
  - Data in the dashboard should be presented in visually pleasing form of interactive plots
  - Option in user's account settings to set up automatic email notifications once per day (e.g. 7am)
    delivering current weather and forecast (as well as air pollution data) for the next 24 hours to their registration email's inbox
- Other important considerations:
  - Free tier of OpenWeatherAPI limits the number of calls to 1e6 / month
  - Therefore, it makes sense to somehow limit the number of API calls a user is allowed to make,
    e.g. by limiting the number of locations that can be tracked in the dashboard
    - 10 places would mean 80 calls per user per day (1 call per location every 3 hours),
      so around 2400-2500 calls per user per month, so at 1e6 calls we could support 400 users.
    - Above calculation doesn't account for calls to [Air Pollution API](https://openweathermap.org/api/air-pollution) and [Geocoding API](https://openweathermap.org/api/geocoding-api)
      so the actual number of possible users would be less
    - However, Free tier should be enough for demonstration purposes
    - **Another important remark** - it actually makes no sense to update data for locations
      not tracked by any authenticated users. We only need to check if some location's data
      needs updating (i.e. last entry for current weather data is older than 3 hours)
      only when any user tracking this location is authenticated or before sending email notification

External supportive sources and tools:
- [Open Weather API](https://openweathermap.org/) + [Air Pollution API](https://openweathermap.org/api/air-pollution) + [Geocoding API](https://openweathermap.org/api/geocoding-api)
- http://geojson.xyz/ for geographic data (**if** we decide to proceed with interactive map feature)
- AWS/ PythonAnywhere/ something else for hosting - demonstration purposes
- A Docker image allowing to provide one's own [Open Weather API](https://openweathermap.org/) key in order to effectively launch
and use the app locally by anyone interested - **if possible**

## Consequences

Requirements will become defined upon acceptance of the present architecture design record.

An actual piece of software fulfilling these requirements will be created, hopefully.

## Keywords

- functionality
- requirements
- authentication
- dashboard
