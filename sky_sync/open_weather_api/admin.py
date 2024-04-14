from django.contrib import admin
from open_weather_api.models import Current, Geolocation, Forecast

admin.site.register(Current)
admin.site.register(Geolocation)
admin.site.register(Forecast)
