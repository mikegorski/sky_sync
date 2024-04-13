from typing import Union
from enum import Enum
import requests
from requests import Response
from requests.exceptions import ConnectionError, RequestException

from open_weather_api.api.exceptions import OpenWeatherAPIException


class APIUrl(Enum):
    DIRECT_GEOCODING = "https://api.openweathermap.org/geo/1.0/direct?"
    REVERSE_GEOCODING = "https://api.openweathermap.org/geo/1.0/reverse?"
    CURRENT_WEATHER = "https://api.openweathermap.org/data/2.5/weather?"
    FORECAST_WEATHER = "https://api.openweathermap.org/data/2.5/forecast?"
    IP = "https://api.ipify.org"


class RequestSender:
    def __init__(self, base_url: APIUrl | None = None):
        self.base_url = base_url

    def set_url(self, base_url: APIUrl):
        self.base_url = base_url

    def _build_url(self, **query_params: Union[str, float]) -> str:
        return self.base_url.value + "&".join([f"{k}={v}" for k, v in query_params.items()])

    def send(self, base_url: APIUrl, **query_params: Union[str, float]) -> Response:
        self.set_url(base_url)
        try:
            resp = requests.get(url=self._build_url(**query_params))
        except (RequestException, ConnectionError) as e:
            raise OpenWeatherAPIException("An error occurred") from e
        return resp
