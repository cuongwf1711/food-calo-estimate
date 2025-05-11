# Copyright (C)
# date: 10-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""Custom Throttle."""

from rest_framework.throttling import SimpleRateThrottle

from utils.split_num_str import split_num_str


class CustomThrottle(SimpleRateThrottle):
    """Custom Throttle."""

    scope_attr = "throttle_rates"

    def __init__(self):
        # Override the usual SimpleRateThrottle, because we can't determine
        # the rate until called by the view.
        pass

    def parse_rate(self, rate):
        """
        Given the request rate string, return a two tuple of:
        <allowed number of requests>, <period of time in seconds>
        """
        if rate is None:
            return (None, None)
        num, num_period = rate.split("/")
        num_p, period = split_num_str(num_period)
        num_requests = int(num)
        duration = {"s": 1, "m": 60, "h": 3600, "d": 86400}[period[0]]
        if not num_p:
            num_p = 1
        total_duration = int(num_p) * duration
        return (num_requests, total_duration)

    def allow_request(self, request, view):
        """Custom allow_request method."""
        current_method = request.method.lower()
        throttle_rates = getattr(view, self.scope_attr, {})

        if current_method not in throttle_rates:
            return True

        self.rate = throttle_rates[current_method]
        self.num_requests, self.duration = self.parse_rate(self.rate)
        return super().allow_request(request, view)

    def get_cache_key(self, request, view):
        """
        If `view.throttle_scope` is not set, don't apply this throttle.

        Otherwise generate the unique cache key by concatenating the user id
        with the `.throttle_scope` property of the view.
        """
        if request.user and request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return self.cache_format % {"scope": "mycustom", "ident": ident}
