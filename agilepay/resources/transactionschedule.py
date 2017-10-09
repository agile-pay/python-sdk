from ..helpers import dicts_merge


class TransactionSchedule:

    def __init__(self, client, reference=None):
        """
        Initialize the transaction schedule resource

        visit http://docs.agilepay.io/#!/transaction-schedule

        :param client:
        :type client: agilepay.client.Client
        :param reference: the scheduled transaction reference
        :type reference: str
        """
        self._client = client
        self._reference = reference
        self._gateway_reference = None
        self._webhook_reference = None
        self._schedule_reference = None
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

    def set_webhook(self, reference):
        """
        Set the webhook reference

        :param reference:
        :type reference: str
        :return:
        :rtype self
        """
        self._webhook_reference = reference
        return self

    def set_schedule(self, reference):
        """
        Set the schedule reference

        :param reference:
        :type reference: str
        :return:
        :rtype self
        """
        self._schedule_reference = reference
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

    def schedule(self, type, at, timezone, data, retries=[]):
        """
        Schedule a transaction to be executed in the future

        :param type: the transaction type to schedule
        :type type: str
        :param at: ex : 2018-12-01 20:00:00
        :type at: str
        :param timezone:
        :type timezone: the timezone Europe/Rome
        :param data:
        :type data: dict
        :param retries:
        :type retries: list
        :return:
        :rtype: agilepay.responses.Response
        """
        not_mandatory = {}
        if len(retries) > 0:
            not_mandatory['retries'] = retries
        if self._gateway_reference is not None:
            not_mandatory['gateway'] = self._gateway_reference
        if self._webhook_reference is not None:
            not_mandatory['webhook'] = self._webhook_reference
        if self._schedule_reference is not None:
            not_mandatory['schedule'] = self._schedule_reference
        if self._payment_method_token is not None:
            not_mandatory['payment_method'] = self._payment_method_token

        return self._client.post('transaction-schedules', {
            'body': dicts_merge({
                'transaction_type': type,
                'schedule_at': at,
                'timezone': timezone,
                'transaction_data': data
            }, not_mandatory)
        })