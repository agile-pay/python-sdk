import json
import datetime

from .helpers import is_json, json_to_dict


class ConfigurationError(Exception):
    pass


class PaginatedResponseError(Exception):
    pass


class HttpError(Exception):

    def __init__(self, http_code, message=None):
        self.http_code = http_code
        if message is not None:
            Exception.__init__(self, "(HTTP code : %s) %s" % (http_code, message))


class UnauthorizedError(HttpError):

    def __init__(self):
        HttpError.__init__(self, 401, "Wrong authentication")


class ForbiddenError(HttpError):
    def __init__(self):
        HttpError.__init__(self, 403, "Forbidden")


class TooManyRequestsError(HttpError):

    def __init__(self, rate_limit, rate_reset):
        self.rate_limit = int(rate_limit)
        self.rate_reset = datetime.datetime.fromtimestamp(int(rate_reset))
        HttpError.__init__(self, 429, "Limit of %d requests reached" % int(rate_limit))


class UnprocessableEntityError(HttpError):

    def __init__(self, errors):
        if is_json(errors):
            self.errors = json_to_dict(errors)
        else:
            self.errors = errors

        HttpError.__init__(self, 422, "The payload contains invalid data")
