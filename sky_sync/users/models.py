from django.db import models
from django.contrib.auth.models import AbstractUser
from open_weather_api.models import Geolocation


class User(AbstractUser):
    last_failed_login_attempt = models.DateTimeField(null=True, default=None)
    last_login = models.DateTimeField(null=True, default=None)
    is_active = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=True, default=None)


class Dashboard(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="dashboard")
    geolocations = models.ManyToManyField(to=Geolocation, blank=True, related_name="dashboards")

    def __str__(self):
        return f"{self.user}'s Dashboard"
