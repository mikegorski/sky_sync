from rest_framework import serializers
from open_weather_api.models import Geolocation, Forecast, Current


class GeolocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geolocation
        fields = '__all__'


class ForecastSerializer(serializers.ModelSerializer):
    geolocation = GeolocationSerializer(many=False)

    class Meta:
        model = Forecast
        fields = '__all__'

    def create(self, validated_data):
        location_data = validated_data.pop("geolocation")
        geolocation, _ = Geolocation.objects.get_or_create(**location_data)
        return Forecast.objects.create(geolocation=geolocation, **validated_data)


class CurrentSerializer(serializers.ModelSerializer):
    geolocation = GeolocationSerializer(many=False)

    class Meta:
        model = Current
        fields = '__all__'

    def create(self, validated_data):
        location_data = validated_data.pop("geolocation")
        geolocation, _ = Geolocation.objects.get_or_create(**location_data)
        current_data_instance, _ = Current.objects.update_or_create(geolocation=geolocation, defaults=validated_data)
        return current_data_instance
