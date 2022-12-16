from statsd.defaults.django import statsd
import random

from django.http import HttpResponse


def say_hello(request):
    http_status_code = random.choice([200, 400, 500, 503])
    statsd.incr('weatherapi.responses.total', tags=[
        'code:{}'.format(http_status_code),
    ])
    return 'It is sunny!'
