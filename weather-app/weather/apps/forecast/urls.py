from django.conf.urls import url

from .views import current_weather

urlpatterns = [
    url(r'^$', current_weather),
]
