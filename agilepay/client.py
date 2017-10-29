import sys
import hmac
import platform
import requests

from time import time
from hashlib import sha256
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
from base64 import b64encode
from collections import OrderedDict

# internal module imports
from .errors import *
from .responses import Response
from .helpers import dict_to_json
from .constants import API_VERSION, SDK_VERSION, ENV_LOCAL, ENV_TESTING, ENV_PRODUCTION


class Client:

    _base_uris = {
        ENV_LOCAL: 'https://api.agilepay.dev/v' + str(API_VERSION) + '/',
        ENV_TESTING: 'https://api.agilepay.dev/v' + str(API_VERSION) + '/',
        ENV_PRODUCTION: 'https://api.agilepay.io/v' + str(API_VERSION) + '/',
    }

    def __init__(self, config):
        """
        Initialize the client

        config['api_key'] -- the api key associated to the agile-pay account
        config['api_secret'] -- the api secret associated to the agile-pay account
        config['environment'] -- production, testing, local

        :param config: dict
        :return: None
        """

        if 'environment' not in config:
            config['environment'] = ENV_PRODUCTION

        self._validate_config(config)
        self._config = config

    def get_config(self):
        """
        Get the configuration entries

        :return:
        :rtype: dict
        """
        return self._config

    def get(self, uri, options={}):
        """
        Make a get request to the agilepay service

        :param uri:
        :type uri: str
        :param options:
        :type options: dict
        :return:
        :rtype: agilepay.responses.Response
        """
        return self.request('get', uri, options)

    def post(self, uri, options={}):
        """
        Make a post request to the agilepay service

        :param uri:
        :type uri: str
        :param options:
        :type options: dict
        :return: Response
        :rtype: agilepay.responses.Response
        """
        return self.request('post', uri, options)

    def put(self, uri, options={}):
        """
        Make a put request to the agilepay service

        :param uri:
        :type uri: str
        :param options:
        :type options: dict
        :return: Response
        :rtype: agilepay.responses.Response
        """
        return self.request('put', uri, options)

    def delete(self, uri, options={}):
        """
        Make a delete request to the agilepay service

        :param uri:
        :type uri: str
        :param options:
        :type options: dict
        :return: Response
        :rtype: agilepay.responses.Response
        """
        return self.request('delete', uri, options)

    def request(self, method, uri, options = {}):
        """
        Make an http request to the agilepay service

        options = {
            query = {},
            headers = {},
        }

        :param method: str the http verb (get,post,put,delete,patch)
        :type method: str
        :param uri: str the uri
        :type uri: str
        :param options: dict the dictionary of key : options
        :type options: dict
        :return:
        :rtype: agilepay.responses.Response
        """

        # initializing full url
        url = self._get_base_uri()+uri
        if 'query' in options:
            options['query'] = OrderedDict(sorted(options['query'].items()))
            url += "?%s" % urlencode(options['query'])

        if 'headers'not in options:
            options['headers'] = {}

        if 'body' in options:
            options['headers']['Accept'] = 'application/json'
            options['headers']['Content-Type'] = 'application/json'
        else:
            options['body'] = {}

        options['headers']['User-Agent'] = self._render_user_agent()

        string_body = dict_to_json(options['body'])

        # calculating request signature
        signature = self._sign_request(method, url, string_body)
        options['headers']['Authorization'] = 'AP %s:%s' % (self._config['api_key'], signature)

        # mapping request options for the requests library
        response = requests.request(method, url, **dict(
            headers=options['headers'],
            verify=True if self._config['environment'] == ENV_PRODUCTION else False,
            data=string_body
        ))

        return self._handle_response(response)

    def _handle_response(self, response):
        http_code = response.status_code
        if http_code in [200, 201, 204]:
            return Response(response)
        elif http_code == 401:
            raise UnauthorizedError()
        elif http_code == 403:
            raise ForbiddenError()
        elif http_code == 422:
            raise UnprocessableEntityError(response.text)
        elif http_code == 429:
            rate_limit = response.headers['X-Ratelimit-Limit']
            rate_reset = response.headers['X-Ratelimit-Reset']
            raise TooManyRequestsError(rate_limit, rate_reset)
        else:
            raise HttpError(http_code, str(http_code)+" : an error has occurred")

    def _render_user_agent(self):
        return 'agile-pay/python/%s python-version:%s os:%s' % (
            SDK_VERSION,
            platform.python_version(),
            platform.platform()
        )

    def _sign_request(self, method, url, body=''):
        concat = method.upper() + url + body + str(int(time()))
        secret = self._config['api_secret']
        if (sys.version_info > (3, 0)):
            secret = bytes(secret, 'utf-8')
            concat = bytes(concat, 'utf-8')
        signer = hmac.new(secret, b64encode(concat), sha256)
        return signer.hexdigest()

    def _get_base_uri(self):
        return self._base_uris[self._config['environment']]

    def _validate_config(self, config):
        required = ['api_key', 'api_secret', 'environment']
        for field in required:
            if field not in field or len(config[field]) < 1:
                raise ConfigurationError('Missing required configuration field : '+field)

        if not config['environment'] in [
            ENV_LOCAL,
            ENV_TESTING,
            ENV_PRODUCTION
        ]:
            raise ConfigurationError('Invalid environment : '+config['environment'])

