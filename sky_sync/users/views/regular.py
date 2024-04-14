from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
from open_weather_api.models import Current, Forecast


class DashboardView(TemplateView, LoginRequiredMixin):
    template_name = 'users/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dashboard = self.request.user.dashboard
        current_weather_data = Current.objects.filter(geolocation__in=dashboard.geolocations.all())
        forecast_weather_data = Forecast.objects.filter(geolocation__in=dashboard.geolocations.all())
        context['current_weather_data'] = current_weather_data
        context['forecast_weather_data'] = forecast_weather_data
        return context

    def get(self, request, *args, **kwargs):
        # check if any data needs updating and queue updates
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class LandingView(TemplateView):
    template_name = 'users/landing_page.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, self.template_name)


class AboutView(TemplateView):
    template_name = 'users/about.html'
