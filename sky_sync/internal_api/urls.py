from django.urls import path
from internal_api.views import AllTrackedCurrentDataView, AllTrackedForecastDataView


urlpatterns = [
    path("current/", AllTrackedCurrentDataView.as_view(), name="tracked-current-weather-data"),
    path("forecast/", AllTrackedForecastDataView.as_view(), name="tracked-forecast-weather-data"),
]
