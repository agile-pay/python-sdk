import hmac

from hashlib import sha256
from base64 import b64encode

from ..helpers import dicts_merge, dict_to_json


class Webhook:

    def __init__(self, client, reference):
        """
        Initialize the webhook resource

        :param client:
        :type client: agilepay.client.Client
        :param reference:
        :type reference: str
        """
        self._client = client
        self._reference = reference

    def set_reference(self, reference):
        """
        Set the webhook reference

        :param reference:
        :type reference: str
        :return:
        :rtype self
        """
        self._reference = reference
        return self

    def create(self, url, options={}):
        """
        Create a new webhook

        :param url:
        :type url: str
        :param options:
        :type options: dict
        :return:
        :rtype: agilepay.responses.Response
        """
        body = dicts_merge(options, {'url': url})
        return self._client.post('webhooks', {
            'body': body
        })

    def update(self, data={}):
        """
        Update a specified webhook

        :param data:
        :type data: dict
        :return:
        :rtype: agilepay.responses.Response
        """
        return self._client.put('webhooks/%s' % self._reference, {
            'body' : data
        })

    def verify_signature(self, signature, body):
        """
        Verifies whether a provided signature from a webhook request is valid

        :param signature: the X-Agilepay-Signature
        :type signature: str
        :param body: the webhook request body
        :type body: dict
        :return:
        :rtype: bool
        """
        secret = self._client.get_config()['api_secret']
        compare = hmac.new(secret, b64encode(dict_to_json(body)), sha256).hexdigest()
        return hmac.compare_digest(signature, compare)
