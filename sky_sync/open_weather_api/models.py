from django.db import models


class Geolocation(models.Model):
    name = models.CharField()
    country = models.CharField()
    state = models.CharField(null=True, default=None)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        s = f"{self.name}, {self.state}, {self.country}" if self.state else f"{self.name}, {self.country}"
        s += f" ({self.lat}, {self.lon})"
        return s


class WeatherData(models.Model):
    dt = models.DateTimeField()
    description = models.CharField()
    icon = models.CharField()
    temperature = models.FloatField()
    temperature_feel = models.FloatField()
    pressure = models.PositiveIntegerField()
    humidity = models.PositiveIntegerField()
    wind_spd = models.FloatField()
    wind_deg = models.PositiveIntegerField()
    rain_3h = models.FloatField(null=True, default=None)
    snow_3h = models.FloatField(null=True, default=None)

    class Meta:
        abstract = True


class Current(WeatherData):
    geolocation = models.OneToOneField(to=Geolocation, on_delete=models.CASCADE, related_name="current_weather_data")
    sunrise = models.DateTimeField()
    sunset = models.DateTimeField()
    rain_1h = models.FloatField(null=True, default=None)
    snow_1h = models.FloatField(null=True, default=None)

    class Meta:
        verbose_name = "Current Weather Datapoint"

    def __str__(self):
        return f"{self.geolocation} @ {self.dt}"


class Forecast(WeatherData):
    geolocation = models.ForeignKey(to=Geolocation, on_delete=models.CASCADE, related_name="forecast_weather_data")

    class Meta:
        ordering = ["geolocation", "dt"]
        verbose_name = "Forecast Weather Datapoint"

    def __str__(self):
        return f"{self.geolocation} @ {self.dt}"
