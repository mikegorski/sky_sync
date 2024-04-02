from django.urls import path
from .views import CurrentWeatherCreateView, ForecastWeatherCreateView

urlpatterns = [
    path("data/current/", CurrentWeatherCreateView.as_view(), name="get-current-weather-data"),
    path("data/forecast/", ForecastWeatherCreateView.as_view(), name="get-forecast-weather-data"),
]
