from django.http import HttpResponse

from .requestor import request_weather_forecast


def current_weather(request):
    forecast = request_weather_forecast('Chiang Mai')
    return HttpResponse(forecast)
