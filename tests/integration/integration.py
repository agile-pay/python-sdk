import random
import datetime

from unittest2 import TestCase as BaseTestCase

from agilepay.client import Client
from agilepay.resources import Gateway
from agilepay.resources import Customer
from agilepay.resources import PaymentMethod

class ResourceTestCase(BaseTestCase):

    def setUp(self):
        """
        :type client: agilepay.client.Client
        """
        super(ResourceTestCase, self).setUp()
        self.client = Client({
            'api_key': 'key',
            'api_secret': 'secret',
            'environment': 'testing'
        })


    def create_dummy_gateway(self):
        """
        Creates a dummy gateway
        :return:
        :rtype: agilepay.responses.Response
        """
        return Gateway(self.client).create('test', {'dummy_key': 'dummy'})

    def create_dummy_customer(self):
        """
        Creates a dummy customer
        :return:
        :rtype: agilepay.responses.Response
        """
        return Customer(self.client).create({
            'email': 'test%s@email.com' % random.random(),
            'last_name': 'Rossi',
            'first_name': 'Mario',
        })

    def create_dummy_payment_method_card(self, options={}):
        """
        Creates a dummy payment method type of card

        :param options:
        :return:
        :rtype: agilepay.responses.Response
        """
        return PaymentMethod(self.client).create_card({
            'cvv': '123',
            'number': '4111111111111111',
            'holder_name': 'Mario Rossi',
            'expiry_year': str(datetime.datetime.now().year)[-2:],
            'expiry_month': '12',
        })

    def create_dummy_payment_method_gateway_token(self, options={}, from_existing=False):
        """
        Creates a dummy payment method type of gateway_token

        :param options:
        :return: agilepay.responses.Response
        """
        gateway = self.create_dummy_gateway().get_body()['reference']
        if not from_existing:
            return PaymentMethod(self.client).create_gateway_token(gateway, {
                'cvv': '123',
                'number': '4111111111111111',
                'holder_name': 'Mario Rossi',
                'expiry_year': str(datetime.datetime.now().year)[-2:],
                'expiry_month': '12',
            })
        else:
            card = self.create_dummy_payment_method_card().get_body()['token']
            return PaymentMethod(self.client, card).create_gateway_token(gateway)
