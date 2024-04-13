from abc import ABC, abstractmethod
from datetime import datetime

from open_weather_api.api.urls import RequestSender
from open_weather_api.api.urls import APIUrl
from sky_sync.settings import API_TOKEN

from requests import Response
from rest_framework.exceptions import ParseError


class BaseProcessor(ABC):
    def __init__(self):
        self.request_sender = RequestSender()

    @abstractmethod
    def _process(self, resp: Response):
        raise NotImplementedError

    @abstractmethod
    def execute(self, **kwargs):
        raise NotImplementedError


class CurrentProcessor(BaseProcessor):
    def _process(self, resp: Response) -> dict:
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

    def execute(self, lat: float, lon: float) -> dict:
        resp = self.request_sender.send(
            base_url=APIUrl.CURRENT_WEATHER, lat=lat, lon=lon, units="metric", limit=5, appid=API_TOKEN
        )
        return self._process(resp)


class ForecastProcessor(BaseProcessor):
    def _process(self, resp) -> list[dict]:
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

    def execute(self, lat: float, lon: float) -> list[dict]:
        resp = self.request_sender.send(
            base_url=APIUrl.FORECAST_WEATHER, lat=lat, lon=lon, units="metric", limit=5, appid=API_TOKEN
        )
        return self._process(resp)
