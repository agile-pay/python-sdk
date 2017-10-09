from ..helpers import dicts_merge
from ..responses import PaginatedResponse


class Transaction:

    def __init__(self, client, reference=None):
        """
        Initialize the transaction resource

        visit http://docs.agilepay.io/#!/transaction

        :param client:
        :type client agilepay.client.Client
        :param reference:
        :type reference: str
        """
        self._client = client
        self._reference = reference
        self._gateway_reference = None
        self._payment_method_token = None

    def set_gateway(self, reference):
        """
        Set the gateway reference

        :param reference:
        :type reference: str
        :return:
        :rtype self
        """
        self._gateway_reference = reference
        return self

    def set_payment_method(self, token):
        """
        Set the payment method token

        :param token:
        :type token: str
        :return:
        :rtype self
        """
        self._payment_method_token = token
        return self

    def get(self):
        """
        Get a transaction

        :return: the response
        :rtype: agilepay.responses.Response
        """
        return self._client.get('transaction/%s' % self._reference)

    def get_list(self, options={}):
        """
        Get the list of transactions executed by the user

        :param options:
        :type options: dict
        :return:
        :rtype: agilepay.responses.PaginatedResponse
        """

        query = {}
        if self._gateway_reference is not None:
            query['gateway'] = self._gateway_reference
        if self._payment_method_token is not None:
            query['payment_method'] = self._payment_method_token

        query = dicts_merge(query, options)
        response = self._client.get('transactions', {'query': query})

        return PaginatedResponse(self._client, response)

    def auth(self, amount, currency, data={}):
        """
        Process an authorise transaction

        visit http://docs.agilepay.io/#!/transaction-authorize

        :param amount: the amount in cents ex: 500 = 5.00
        :type amount: int
        :param currency: the currency code GBP, EUR ..
        :type currency: str
        :param data: specify further data
        :type data: dict
        :return:
        :rtype: agilepay.responses.Response
        """
        body = {
            'amount': amount,
            'currency_code': currency,
            'payment_method': self._payment_method_token
        }

        if self._gateway_reference is not None:
            body['gateway'] = self._gateway_reference

        body = dicts_merge(body, data)

        return self._client.post('transaction/auth', {'body': body})

    def void(self):
        """
        Void an authorised transaction

        visit http://docs.agilepay.io/#!/transaction-void

        :return:
        :rtype: agilepay.responses.Response
        """
        return self._client.post('transaction/%s/void' % self._reference)

    def capture(self, amount=None, currency=None):
        """
        Capture an authorised transaction

        visit http://docs.agilepay.io/#!/transaction-capture

        :param amount: the amount to capture
        :type amount: int
        :param currency: the currency code
        :type currency: str
        :return:
        :rtype: agilepay.responses.Response
        """
        body = {}
        if amount is not None:
            body['amount'] = amount
        if currency is not None:
            body['currency_code'] = currency

        return self._client.post('transaction/%s/capture' % self._reference, {
            'body': body
        })

    def credit(self, amount=None, currency=None):
        """
        Credit a captured transaction

        visit http://docs.agilepay.io/#!/transaction-credit

        :param amount: the amount to credit
        :type amount: int
        :param currency: the currency code
        :type currency: str
        :return:
        :rtype: agilepay.responses.Response
        """
        body = {}
        if amount is not None:
            body['amount'] = amount
        if currency is not None:
            body['currency_code'] = currency

        return self._client.post('transaction/%s/credit' % self._reference, {
            'body': body
        })