"""
weather.common.statsd
~~~~~~~~~~~~~~~~~~~~~

StatsD client is configured here. We use Datadog's StatsD fork, because it
supports metric tagging. Usage example::

    >>> from weather.common.statsd import statsd
    >>> statsd.increment('api.responses.total', tags=['status_code:200'])

"""
import time

from datadog import DogStatsd

from django.conf import settings

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    class MiddlewareMixin(object):
        pass

statsd = DogStatsd(
    host=getattr(settings, 'STATSD_HOST', "localhost"),
    port=getattr(settings, 'STATSD_PORT', 8125),
    namespace=getattr(settings, 'STATSD_PREFIX', None)
)


class RequestLatencyMiddleware(MiddlewareMixin):
    """The middleware measures time in seconds spent serving HTTP requests.

    Put the middleware to the top in the MIDDLEWARE_CLASSES, so it runs before
    all middlewares on request phase and last on response phase.

    Do not use labels to store dimensions with high cardinality, e.g.,
    /v1/books/<book-id> path.

    """

    def process_request(self, request):
        request._begun_at = time.time()

    def process_response(self, request, response):
        if not hasattr(request, '_begun_at'):
            return response

        took_seconds = time.time() - request._begun_at
        statsd.histogram('request.duration.seconds', took_seconds, tags=[
            'method:{}'.format(request.method),
            'path:{}'.format(request.path),
            'status_code:{}'.format(response.status_code),
        ])
        return response
