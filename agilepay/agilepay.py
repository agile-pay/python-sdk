import resources

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
        return resources.Credit(self._client)

    def gateway(self, reference=None):
        """
        Access the gateway resource

        :param reference:
        :return: the gateway resource
        :rtype: agilepay.resources.Gateway
        """
        return resources.Gateway(self._client, reference)

    def webhook(self, reference=None):
        """
        Access the webhook resource

        :param reference:
        :return: the webhook resource
        :rtype: agilepay.resources.Webhook
        """
        return resources.Webhook(self._client, reference)

    def schedule(self, reference=None):
        """
        Access the schedule resource

        :param reference:
        :return: the schedule resource
        :rtype: agilepay.resources.Schedule
        """
        return resources.Schedule(self._client, reference)

    def transaction(self, reference=None):
        """
        Access the transaction resource

        :param reference:
        :return: the transaction resource
        :rtype: agilepay.resources.Transaction
        """
        return resources.Transaction(self._client, reference)

    def payment_method(self, token=None):
        """
        Access the payment method resource

        :param token:
        :type token: str
        :return: the payment method resource
        :rtype: agilepay.resources.PaymentMethod
        """
        return resources.PaymentMethod(self._client, token)

    def transaction_schedule(self, reference=None):
        """
        Access the transaction schedule resource

        :param reference:
        :type reference: str
        :return: the transaction schedule resource
        :rtype: agilepay.resources.TransactionSchedule
        """
        return resources.TransactionSchedule(self._client, reference)