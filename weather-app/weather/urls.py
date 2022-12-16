from django.conf.urls import url, include
from django.contrib import admin
from django.http import HttpResponse

urlpatterns = [
    url(r'^healthz$', view=lambda request: HttpResponse('ok')),
    url(r'^forecast', include('weather.apps.forecast.urls')),
    url(r'^admin/', admin.site.urls),
]
