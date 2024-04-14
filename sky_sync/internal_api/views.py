from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from open_weather_api.models import Current, Forecast
from open_weather_api.serializers import CurrentSerializer, ForecastSerializer
from rest_framework.filters import SearchFilter


class AllTrackedCurrentDataView(ListAPIView):
    serializer_class = CurrentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['geolocation__name']

    def get_queryset(self):
        user = self.request.user
        geolocations = user.dashboard.geolocations.all()
        return Current.objects.filter(geolocation__in=geolocations)


class AllTrackedForecastDataView(ListAPIView):
    serializer_class = ForecastSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['geolocation__name']

    def get_queryset(self):
        user = self.request.user
        geolocations = user.dashboard.geolocations.all()
        return Forecast.objects.filter(geolocation__in=geolocations)
