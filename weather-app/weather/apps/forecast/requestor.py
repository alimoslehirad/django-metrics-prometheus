import random

from weather.common.statsd import statsd


def request_weather_forecast(location):
    http_status_code = random.choice([200, 400, 500, 503])
    statsd.increment('weatherapi.responses.total', tags=[
        'code:{}'.format(http_status_code),
    ])
    return 'It is sunny!'
