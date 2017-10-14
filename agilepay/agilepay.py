from .resources import *

from .client import Client


class AgilePay:

    def __init__(self, config={}):
        """
        Initialize the agilepay sdk

        :param config:
        """
        self._client = Client(config)

    def credit(self):
        """
        Access the credit resource

        :return:
        :rtype: agilepay.resources.Credit
        """
        return Credit(self._client)

    def gateway(self, reference=None):
        """
        Access the gateway resource

        :param reference:
        :return: the gateway resource
        :rtype: agilepay.resources.Gateway
        """
        return Gateway(self._client, reference)

    def webhook(self, reference=None):
        """
        Access the webhook resource

        :param reference:
        :return: the webhook resource
        :rtype: agilepay.resources.Webhook
        """
        return Webhook(self._client, reference)

    def schedule(self, reference=None):
        """
        Access the schedule resource

        :param reference:
        :return: the schedule resource
        :rtype: agilepay.resources.Schedule
        """
        return Schedule(self._client, reference)

    def transaction(self, reference=None):
        """
        Access the transaction resource

        :param reference:
        :return: the transaction resource
        :rtype: agilepay.resources.Transaction
        """
        return Transaction(self._client, reference)

    def payment_method(self, token=None):
        """
        Access the payment method resource

        :param token:
        :type token: str
        :return: the payment method resource
        :rtype: agilepay.resources.PaymentMethod
        """
        return PaymentMethod(self._client, token)

    def transaction_schedule(self, reference=None):
        """
        Access the transaction schedule resource

        :param reference:
        :type reference: str
        :return: the transaction schedule resource
        :rtype: agilepay.resources.TransactionSchedule
        """
        return TransactionSchedule(self._client, reference)