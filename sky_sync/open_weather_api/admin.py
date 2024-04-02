from django.contrib import admin
from .models import Current, Geolocation, Forecast

admin.site.register(Current)
admin.site.register(Geolocation)
admin.site.register(Forecast)
