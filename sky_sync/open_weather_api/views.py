import json
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from open_weather_api.serializers import CurrentSerializer, ForecastSerializer
from open_weather_api.models import Forecast
from open_weather_api.comm import get_current_weather_data, get_forecast_weather_data
from django.db import transaction


class CurrentWeatherCreateView(CreateAPIView):
    serializer_class = CurrentSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        lat, lon = body.get("lat"), body.get("lon")
        if not lat or not lon:
            raise ParseError(code=400)
        data = get_current_weather_data(lat, lon)
        serializer = self.get_serializer(data=data, context={"request": request}, many=False)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ForecastWeatherCreateView(CreateAPIView):
    serializer_class = ForecastSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Forecast.objects.all()

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        lat, lon = body.get("lat"), body.get("lon")
        if not lat or not lon:
            raise ParseError(code=400)
        data = get_forecast_weather_data(lat, lon)
        serializer = self.get_serializer(data=data, context={"request": request}, many=True)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            self.queryset.filter(geolocation__lat=lat, geolocation__lon=lon).delete()
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
