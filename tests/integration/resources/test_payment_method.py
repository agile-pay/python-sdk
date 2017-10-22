import datetime

from ..integration import ResourceTestCase

from agilepay.resources.paymentmethod import PaymentMethod


class PaymentMethodTest(ResourceTestCase):

    def setUp(self):
        """
        :type payment_method: agilepay.resources.paymentmethod.PaymentMethod
        :return:
        """
        super(PaymentMethodTest, self).setUp()
        self.payment_method = PaymentMethod(self.client)

    def test_get(self):
       token = self.create_dummy_payment_method_card().get_body()['token']
       get = self.payment_method.set_token(token).get()
       self.assertEqual(get.get_status_code(), 200)
       self.assertEqual(get.get_body()['token'], token)

    def test_get_list(self):
        list = self.payment_method.get_list()
        self.assertEqual(list.get_response().get_status_code(), 200)

    def test_create_card(self):
        created = self.create_dummy_payment_method_card()
        self.assertEqual(created.get_status_code(), 200)
        self.assertTrue('token' in created.get_body())

    def test_create_gateway_token(self):
        # test success with existing payment method
        created = self.create_dummy_payment_method_gateway_token(from_existing=True)
        self.assertEqual(created.get_status_code(), 200)
        self.assertTrue('token' in created.get_body())
        # test success by passing a new card
        created = self.create_dummy_payment_method_gateway_token(from_existing=False)
        self.assertEqual(created.get_status_code(), 200)
        self.assertTrue('token' in created.get_body())