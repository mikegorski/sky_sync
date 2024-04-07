from datetime import datetime
import os

import requests
from requests import Response
from requests.exceptions import ConnectionError, RequestException
from rest_framework.exceptions import ParseError

from open_weather_api.api_urls import (
    build_current_weather_url,
    build_direct_geocoding_url,
    build_forecast_weather_url,
    build_ip_url,
    build_reverse_geocoding_url,
)
from sky_sync.settings import API_TOKEN


def handle_request(url: str) -> Response:
    """Handles GET requests with possible errors."""
    try:
        resp = requests.get(url=url)
    except (RequestException, ConnectionError):
        print("[bold red]An error occurred. Please check your network connection and try again.[/]")
        exit(1)
    return resp


def get_current_weather_data(lat: float, lon: float) -> dict[str, str | float | dict]:
    resp = handle_request(url=build_current_weather_url(lat=lat, lon=lon, units="metric", limit=5, appid=API_TOKEN))
    data = resp.json()
    if resp.status_code != 200:
        raise ParseError(code=resp.status_code)
    location_data = {
        "name": data["name"],
        "country": data["sys"]["country"],
        "state": None,
        "lat": data["coord"]["lat"],
        "lon": data["coord"]["lon"],
    }
    rain: dict = data.get("rain", {})
    snow: dict = data.get("snow", {})
    current_data = {
        "dt": datetime.fromtimestamp(data["dt"]),
        "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]),
        "sunset": datetime.fromtimestamp(data["sys"]["sunset"]),
        "description": ''.join([x["description"] for x in data["weather"]]),
        "icon": ''.join([x["icon"] for x in data["weather"]]),
        "temperature": data["main"]["temp"],
        "temperature_feel": data["main"]["feels_like"],
        "pressure": data["main"]["pressure"],
        "humidity": data["main"]["humidity"],
        "wind_spd": data["wind"]["speed"],
        "wind_deg": data["wind"]["deg"],
        "rain_1h": rain.get("1h"),
        "snow_1h": snow.get("1h"),
        "rain_3h": rain.get("3h"),
        "snow_3h": snow.get("3h"),
    }

    return {"geolocation": location_data, **current_data}


def get_forecast_weather_data(lat: float, lon: float) -> list[dict[str, str | float | dict]]:
    resp = handle_request(url=build_forecast_weather_url(lat=lat, lon=lon, units="metric", limit=5, appid=API_TOKEN))
    data = resp.json()
    loc = data["city"]
    location_data = {
        "name": loc["name"],
        "country": loc["country"],
        "state": None,
        "lat": loc["coord"]["lat"],
        "lon": loc["coord"]["lon"],
    }
    forecast_data: list[dict] = []
    for forecast in data["list"]:
        params = forecast["main"]
        datapoint: dict = {
            "dt": datetime.fromtimestamp(forecast["dt"]),
            "description": ''.join([x["description"] for x in forecast["weather"]]),
            "icon": ''.join([x["icon"] for x in forecast["weather"]]),
            "temperature": params["temp"],
            "temperature_feel": params["feels_like"],
            "pressure": params["pressure"],
            "humidity": params["humidity"],
            "wind_spd": forecast["wind"]["speed"],
            "wind_deg": forecast["wind"]["deg"],
            "rain_3h": forecast.get("rain", {}).get("3h"),
            "snow_3h": forecast.get("snow", {}).get("3h"),
        }
        forecast_data.append({"geolocation": location_data, **datapoint})
    return forecast_data


def determine_location_based_on_ip(ip: str) -> tuple[float, float]:
    # https://docs.djangoproject.com/en/5.0/ref/contrib/gis/geoip2/#example
    raise NotImplementedError
    # ip = get_ip_address()
    # response = DbIpCity.get(ip_address=ip, api_key="free")
    # lat, lon = float(str(response.latitude)), float(str(response.longitude))
    # locs = get_locations_by_coords(lat, lon, token=api_token)
    # return (ip, locs[0]) if locs else (ip, None)


# def get_locations_by_name(name: str, token: str) -> list[Geolocation]:
#     resp = handle_request(url=build_direct_geocoding_url(q=name, limit=5, appid=token))
#     if resp.status_code != 200:
#         return []
#     locs: list[Geolocation] = []
#     for loc in resp.json():
#         if "state" not in loc:
#             loc["state"] = ""
#         locs.append(
#             Geolocation(name=loc["name"], country=loc["country"], state=loc["state"], lat=loc["lat"], lon=loc["lon"])
#         )
#     return locs


# def get_locations_by_coords(lat: float, lon: float, token: str) -> list[Geolocation]:
#     resp = handle_request(url=build_reverse_geocoding_url(lat=lat, lon=lon, limit=5, appid=token))
#     if resp.status_code != 200:
#         return []
#     locs: list[Geolocation] = []
#     for loc in resp.json():
#         if "state" not in loc:
#             loc["state"] = ""
#         locs.append(
#             Geolocation(name=loc["name"], country=loc["country"], state=loc["state"], lat=loc["lat"], lon=loc["lon"])
#         )
#     return locs
